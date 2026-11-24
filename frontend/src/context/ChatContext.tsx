import {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
  useCallback,
  type ReactNode,
} from 'react'
import type {
  ChatMessage,
  Conversation,
  ConversationSummary,
  ConversationMessage,
} from '@/types'
import {
  chatApi,
  conversationsApi,
  filesApi,
  embeddingsApi,
  type ChatRequest,
  type ChatHistoryMessage,
} from '@/services/api'
import { useEmbedding } from '@/context/EmbeddingContext'

const SESSION_STORAGE_KEY = 'research_rover_active_convo_id'

const getStoredConvoId = (): string | null => {
  try {
    return sessionStorage.getItem(SESSION_STORAGE_KEY)
  } catch {
    return null
  }
}

const setStoredConvoId = (id: string | null) => {
  try {
    if (id) {
      sessionStorage.setItem(SESSION_STORAGE_KEY, id)
    } else {
      sessionStorage.removeItem(SESSION_STORAGE_KEY)
    }
  } catch {
    // Ignore storage availability errors
  }
}

const initialMessage: ChatMessage = {
  id: '1',
  type: 'assistant',
  content:
    "Hello! I'm your AI research assistant. I can help you analyze and understand research papers, summarize methodologies, extract insights, and explain complex concepts.\n\nSelect a collection to ground my answers in your indexed papers, or ask any research question directly.",
  timestamp: Date.now() - 60000,
}

const getInitialDatasetMessage = (filename: string): ChatMessage => ({
  id: `init-${filename}`,
  type: 'assistant',
  content: `Hello! I'm ready to answer questions about **${filename}**.\n\nAsk about methodologies, findings, datasets, limitations, or comparisons between papers in this collection.`,
  timestamp: Date.now(),
})

const mapConversationMessageToChatMessage = (m: ConversationMessage): ChatMessage => ({
  id: m.id,
  type: m.role as 'user' | 'assistant',
  content: m.content,
  timestamp: new Date(m.created_at).getTime(),
  isError: m.is_error,
  sources: m.sources || [],
  conversation_id: m.conversation_id,
})

const mapErrorToUserFriendly = (rawError: any): string => {
  const errStr = String(rawError || '').toLowerCase()
  if (
    errStr.includes('429') ||
    errStr.includes('resource_exhausted') ||
    errStr.includes('quota') ||
    errStr.includes('rate limit')
  ) {
    return 'The AI model rate limit was reached. Please wait a moment and try again.'
  }
  if (
    errStr.includes('503') ||
    errStr.includes('unavailable') ||
    errStr.includes('overloaded')
  ) {
    return 'The AI service is temporarily overloaded or unavailable. Please retry in a few moments.'
  }
  if (errStr.includes('dataset mismatch')) {
    return rawError
  }
  if (errStr.includes('timeout') || errStr.includes('120000ms')) {
    return 'The request timed out while analyzing your papers. Please try asking a more specific question, or retry.'
  }
  if (errStr.includes('network error') || errStr.includes('econnrefused') || errStr.includes('failed to fetch')) {
    return 'Unable to connect to the Research Rover backend service. Please ensure the backend is running.'
  }
  return rawError || 'Failed to generate response'
}

interface ChatContextValue {
  messages: ChatMessage[]
  inputMessage: string
  setInputMessage: (v: string) => void
  selectedFile: string | null
  setSelectedFile: (f: string | null) => void
  availableFiles: string[]
  /** Add a filename to the dropdown (if missing) and select it. */
  addAvailableFile: (filename: string) => void
  isLoading: boolean
  streamingStatus: string | null
  error: string
  setError: (e: string) => void
  hasEmbeddings: boolean
  sendMessage: (customText?: string) => Promise<void>
  stopGeneration: () => void
  regenerateResponse: () => Promise<void>
  clearConversation: () => void

  // ─── Phase 3B Persistent Conversation Management ───────────────────────────
  activeConversationId: string | null
  conversations: ConversationSummary[]
  isLoadingConversations: boolean
  isLoadingMessages: boolean
  conversationError: string | null
  loadConversations: (dataset?: string | null) => Promise<void>
  createConversation: (title?: string, dataset?: string | null) => Promise<Conversation | null>
  createNewConversation: (title?: string, dataset?: string | null) => Promise<Conversation | null>
  openConversation: (id: string) => Promise<void>
  selectConversation: (id: string) => Promise<void>
  renameConversation: (id: string, title: string) => Promise<void>
  deleteConversation: (id: string) => Promise<void>
  refreshConversations: () => Promise<void>
}

const ChatContext = createContext<ChatContextValue | undefined>(undefined)

/**
 * Holds persistent chat + embedding state above the router so the selected file,
 * active conversation session, and in-flight embedding jobs all survive page navigation
 * and browser refreshes.
 *
 * Messages and conversations are persistently stored and backed by the FastAPI + SQLite
 * backend layer.
 */
export function ChatProvider({ children }: { children: ReactNode }) {
  const { isCreating, completedFile } = useEmbedding()
  const [selectedFile, setSelectedFile] = useState<string | null>(null)
  const [activeConversationId, setActiveConversationId] = useState<string | null>(() => getStoredConvoId())
  const [conversations, setConversations] = useState<ConversationSummary[]>([])
  const [messages, setMessages] = useState<ChatMessage[]>([initialMessage])
  const [isLoadingConversations, setIsLoadingConversations] = useState(false)
  const [isLoadingMessages, setIsLoadingMessages] = useState(false)
  const [conversationError, setConversationError] = useState<string | null>(null)

  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [streamingStatus, setStreamingStatus] = useState<string | null>(null)
  const [availableFiles, setAvailableFiles] = useState<string[]>([])
  const [error, setError] = useState('')
  const [hasEmbeddings, setHasEmbeddings] = useState(false)

  const abortControllerRef = useRef<AbortController | null>(null)
  const activeConvoIdRef = useRef<string | null>(activeConversationId)
  activeConvoIdRef.current = activeConversationId

  // Load available CSV files once on mount
  useEffect(() => {
    filesApi
      .list()
      .then((files) => {
        setAvailableFiles(
          files.filter((f) => f.filename.endsWith('.csv')).map((f) => f.filename)
        )
      })
      .catch((err) => console.error('Error loading files:', err))
  }, [])

  // When an embedding job finishes, auto-select it
  useEffect(() => {
    if (!completedFile) return
    setAvailableFiles((prev) =>
      prev.includes(completedFile) ? prev : [completedFile, ...prev]
    )
    setSelectedFile(completedFile)
  }, [completedFile])

  // Refresh embedding status when selectedFile changes
  useEffect(() => {
    if (!selectedFile) {
      setHasEmbeddings(false)
      return
    }
    let cancelled = false
    embeddingsApi
      .getStatus(selectedFile)
      .then((status) => {
        if (!cancelled) setHasEmbeddings(status.embeddings_exist)
      })
      .catch(() => {
        if (!cancelled) setHasEmbeddings(false)
      })
    return () => {
      cancelled = true
    }
  }, [selectedFile, completedFile])

  // ─── Persistent Conversation Actions ────────────────────────────────────────

  const currentFilterRef = useRef<string | null | undefined>(undefined)

  const loadConversations = useCallback(async (datasetFilter?: string | null) => {
    setIsLoadingConversations(true)
    currentFilterRef.current = datasetFilter
    try {
      let allItems: ConversationSummary[] = []
      let offset = 0
      const limit = 50
      let total = 0

      // Page through all results if total > limit to ensure complete list retrieval
      do {
        const res = await conversationsApi.list(datasetFilter ?? undefined, limit, offset)
        allItems = [...allItems, ...(res.conversations || [])]
        total = res.total || 0
        offset += limit
      } while (allItems.length < total && offset < total)

      setConversations(allItems)
      setConversationError(null)
    } catch (err: any) {
      console.error('Failed to load conversations:', err)
      setConversationError(err?.error || err?.message || 'Failed to load conversations')
    } finally {
      setIsLoadingConversations(false)
    }
  }, [])

  const refreshConversations = useCallback(async () => {
    await loadConversations(currentFilterRef.current)
  }, [loadConversations])

  const openConversation = useCallback(async (conversationId: string) => {
    if (!conversationId) return

    // Abort any in-flight generation
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    setIsLoading(false)
    setStreamingStatus(null)
    setError('')

    // Immediately update active ID and indicate loading
    setActiveConversationId(conversationId)
    setStoredConvoId(conversationId)
    setIsLoadingMessages(true)
    setConversationError(null)

    try {
      const convo = await conversationsApi.get(conversationId)

      // Guard against race conditions if another conversation was opened while awaiting
      if (activeConvoIdRef.current !== conversationId) return

      // Synchronize dataset association
      if (convo.dataset_filename) {
        setSelectedFile(convo.dataset_filename)
        setAvailableFiles((prev) =>
          prev.includes(convo.dataset_filename!) ? prev : [convo.dataset_filename!, ...prev]
        )
      } else {
        setSelectedFile(null)
      }

      if (convo.messages && convo.messages.length > 0) {
        setMessages(convo.messages.map(mapConversationMessageToChatMessage))
      } else {
        setMessages([
          convo.dataset_filename ? getInitialDatasetMessage(convo.dataset_filename) : initialMessage,
        ])
      }
    } catch (err: any) {
      console.error(`Failed to load conversation ${conversationId}:`, err)
      setConversationError(err?.error || err?.message || 'Failed to load conversation')
      // Reset fallback message state
      setMessages([
        selectedFile ? getInitialDatasetMessage(selectedFile) : initialMessage,
      ])
      throw err
    } finally {
      setIsLoadingMessages(false)
    }
  }, [selectedFile])

  const createConversation = useCallback(async (
    title?: string,
    dataset?: string | null
  ): Promise<Conversation | null> => {
    setIsLoadingConversations(true)
    try {
      const targetDataset = dataset !== undefined ? dataset : selectedFile
      const newConvo = await conversationsApi.create({
        title: title || 'New Conversation',
        dataset_filename: targetDataset || null,
      })

      setActiveConversationId(newConvo.id)
      setStoredConvoId(newConvo.id)

      setMessages([
        newConvo.dataset_filename ? getInitialDatasetMessage(newConvo.dataset_filename) : initialMessage,
      ])
      setConversationError(null)

      // Refresh list in background
      refreshConversations()
      return newConvo
    } catch (err: any) {
      console.error('Failed to create conversation:', err)
      setConversationError(err?.error || err?.message || 'Failed to create conversation')
      return null
    } finally {
      setIsLoadingConversations(false)
    }
  }, [selectedFile, refreshConversations])

  const renameConversation = useCallback(async (conversationId: string, newTitle: string) => {
    if (!conversationId || !newTitle.trim()) return
    try {
      const updated = await conversationsApi.rename(conversationId, newTitle.trim())
      setConversations((prev) =>
        prev.map((c) =>
          c.id === conversationId ? { ...c, title: updated.title, updated_at: updated.updated_at } : c
        )
      )
    } catch (err: any) {
      console.error(`Failed to rename conversation ${conversationId}:`, err)
      setConversationError(err?.error || err?.message || 'Failed to rename conversation')
      throw err
    }
  }, [])

  const deleteConversation = useCallback(async (conversationId: string) => {
    if (!conversationId) return
    try {
      await conversationsApi.delete(conversationId)
      setConversations((prev) => prev.filter((c) => c.id !== conversationId))

      // If the active conversation was deleted, clear active state and show welcome message
      if (activeConversationId === conversationId) {
        setActiveConversationId(null)
        setStoredConvoId(null)
        setMessages([
          selectedFile ? getInitialDatasetMessage(selectedFile) : initialMessage,
        ])
      }
    } catch (err: any) {
      console.error(`Failed to delete conversation ${conversationId}:`, err)
      setConversationError(err?.error || err?.message || 'Failed to delete conversation')
      throw err
    }
  }, [activeConversationId, selectedFile])

  // Restore conversation after browser refresh on startup
  useEffect(() => {
    loadConversations(undefined).then(() => {
      const storedId = getStoredConvoId()
      if (storedId) {
        openConversation(storedId).catch(() => {
          setStoredConvoId(null)
          setActiveConversationId(null)
        })
      }
    })
  }, [loadConversations, openConversation])

  // Dataset switching handler ensuring conversation isolation
  const handleSetSelectedFile = (file: string | null) => {
    if (file === selectedFile) return
    setSelectedFile(file)

    // Unbind active conversation if bound to a different dataset to avoid cross-dataset contamination
    setActiveConversationId(null)
    setStoredConvoId(null)
    setMessages([
      file ? getInitialDatasetMessage(file) : initialMessage,
    ])
    setError('')
    setConversationError(null)
  }

  const addAvailableFile = (filename: string) => {
    setAvailableFiles((prev) =>
      prev.includes(filename) ? prev : [filename, ...prev]
    )
    handleSetSelectedFile(filename)
  }

  const stopGeneration = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    setStreamingStatus(null)
    setIsLoading(false)
  }

  const sendMessage = async (customText?: string) => {
    const textToSend = (customText ?? inputMessage).trim()
    if (!textToSend || isCreating || isLoading) return

    // Abort any existing in-flight request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    const controller = new AbortController()
    abortControllerRef.current = controller

    let currentConvoId = activeConversationId

    // Auto-create persistent conversation if not yet initialized
    if (!currentConvoId) {
      try {
        const created = await conversationsApi.create({
          title: 'New Conversation',
          dataset_filename: selectedFile || null,
        })
        currentConvoId = created.id
        setActiveConversationId(created.id)
        setStoredConvoId(created.id)
      } catch (createErr) {
        console.warn('Failed to auto-create conversation session, continuing with stateless fallback:', createErr)
      }
    }

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: textToSend,
      timestamp: Date.now(),
      conversation_id: currentConvoId || undefined,
    }

    const assistantTempId = `asst-${Date.now()}`
    const assistantMessage: ChatMessage = {
      id: assistantTempId,
      type: 'assistant',
      content: '',
      timestamp: Date.now(),
      sources: [],
      conversation_id: currentConvoId || undefined,
      isStreaming: true,
    }

    // Optimistically update message list with user query and streaming placeholder
    setMessages((prev) => [
      ...prev.filter((m) => !m.id.startsWith('init-') && m.id !== '1'),
      userMessage,
      assistantMessage,
    ])

    if (!customText) {
      setInputMessage('')
    }
    setIsLoading(true)
    setStreamingStatus('Searching paper embeddings...')
    setError('')

    // Collect recent 6 turns for conversational context
    const currentHistory = messages.filter(
      (m) =>
        (m.type === 'user' || m.type === 'assistant') &&
        !m.id.startsWith('init-') &&
        m.id !== '1'
    )
    const historyPayload: ChatHistoryMessage[] = currentHistory
      .slice(-6)
      .map((m) => ({
        role: m.type as 'user' | 'assistant',
        content: m.content,
      }))

    let accumulatedText = ''

    try {
      const chatRequest: ChatRequest = {
        message: textToSend,
        filename: selectedFile || undefined,
        history: historyPayload,
        conversation_id: currentConvoId || undefined,
      }

      await chatApi.streamMessage(chatRequest, {
        signal: controller.signal,
        onStatus: (statusPayload) => {
          if (currentConvoId && activeConvoIdRef.current !== currentConvoId) return
          if (statusPayload?.message) {
            setStreamingStatus(statusPayload.message)
          }
        },
        onCitations: (sources) => {
          if (currentConvoId && activeConvoIdRef.current !== currentConvoId) return
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantTempId ? { ...m, sources } : m))
          )
        },
        onDelta: (token) => {
          if (currentConvoId && activeConvoIdRef.current !== currentConvoId) return
          accumulatedText += token
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantTempId
                ? { ...m, content: accumulatedText }
                : m
            )
          )
        },
        onDone: (donePayload) => {
          if (currentConvoId && activeConvoIdRef.current !== currentConvoId) return
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantTempId
                ? {
                    ...m,
                    id: donePayload.message_id || m.id,
                    conversation_id: donePayload.conversation_id || m.conversation_id,
                    isStreaming: false,
                  }
                : m
            )
          )
          refreshConversations()
        },
        onError: (errorPayload) => {
          if (currentConvoId && activeConvoIdRef.current !== currentConvoId) return
          const userFriendly = mapErrorToUserFriendly(errorPayload?.error)
          setError(userFriendly)
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantTempId
                ? {
                    ...m,
                    content: accumulatedText.trim()
                      ? `${accumulatedText.trim()}\n\n**Generation error:** ${userFriendly}`
                      : `**Generation error:** ${userFriendly}`,
                    isError: true,
                    isStreaming: false,
                  }
                : m
            )
          )
        },
      })
    } catch (err: any) {
      if (currentConvoId && activeConvoIdRef.current !== currentConvoId) {
        return
      }

      if (controller.signal.aborted || err?.name === 'AbortError' || err?.message === 'canceled') {
        const stoppedText = accumulatedText.trim()
          ? `${accumulatedText.trim()}\n\n*[Generation stopped by user]*`
          : '*[Generation stopped by user]*'

        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantTempId
              ? {
                  ...m,
                  content: stoppedText,
                  isStreaming: false,
                }
              : m
          )
        )
        return
      }

      const userFriendlyError = mapErrorToUserFriendly(err?.message || err?.error || err?.detail)
      setError(userFriendlyError)

      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantTempId
            ? {
                ...m,
                content: accumulatedText.trim()
                  ? `${accumulatedText.trim()}\n\n**Generation error:** ${userFriendlyError}`
                  : `**Generation error:** ${userFriendlyError}`,
                isError: true,
                isStreaming: false,
              }
            : m
        )
      )
    } finally {
      if (abortControllerRef.current === controller) {
        abortControllerRef.current = null
      }
      setStreamingStatus(null)
      setIsLoading(false)
    }
  }

  const regenerateResponse = async () => {
    if (isLoading || isCreating) return

    const lastUserMsg = [...messages].reverse().find((m) => m.type === 'user')
    if (!lastUserMsg) return

    const userMsgIndex = messages.lastIndexOf(lastUserMsg)
    if (userMsgIndex >= 0) {
      setMessages(messages.slice(0, userMsgIndex))
    }

    await sendMessage(lastUserMsg.content)
  }

  const clearConversation = () => {
    stopGeneration()
    setActiveConversationId(null)
    setStoredConvoId(null)
    setMessages([
      selectedFile ? getInitialDatasetMessage(selectedFile) : initialMessage,
    ])
    setError('')
    setConversationError(null)
  }

  const value: ChatContextValue = {
    messages,
    inputMessage,
    setInputMessage,
    selectedFile,
    setSelectedFile: handleSetSelectedFile,
    availableFiles,
    addAvailableFile,
    isLoading,
    streamingStatus,
    error,
    setError,
    hasEmbeddings,
    sendMessage,
    stopGeneration,
    regenerateResponse,
    clearConversation,

    // Phase 3B/3C Persistent Conversation Management
    activeConversationId,
    conversations,
    isLoadingConversations,
    isLoadingMessages,
    conversationError,
    loadConversations,
    createConversation,
    createNewConversation: createConversation,
    openConversation,
    selectConversation: openConversation,
    renameConversation,
    deleteConversation,
    refreshConversations,
  }

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}

export function useChat() {
  const ctx = useContext(ChatContext)
  if (!ctx) throw new Error('useChat must be used within a ChatProvider')
  return ctx
}
