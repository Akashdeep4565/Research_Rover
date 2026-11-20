import {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
  type ReactNode,
} from 'react'
import type { ChatMessage } from '@/types'
import { chatApi, filesApi, embeddingsApi, type ChatRequest } from '@/services/api'
import { useEmbedding } from '@/context/EmbeddingContext'

const initialMessage: ChatMessage = {
  id: '1',
  type: 'assistant',
  content:
    "Hello! I'm your AI research assistant. I can help you analyze and understand research papers, summarize methodologies, extract insights, and explain complex concepts.\n\nSelect a collection to ground my answers in your indexed papers, or ask any research question directly.",
  timestamp: Date.now() - 60000,
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
  error: string
  setError: (e: string) => void
  hasEmbeddings: boolean
  sendMessage: (customText?: string) => Promise<void>
  stopGeneration: () => void
  regenerateResponse: () => Promise<void>
  clearConversation: () => void
}

const ChatContext = createContext<ChatContextValue | undefined>(undefined)

/**
 * Holds chat + embedding state above the router so the selected file, the
 * conversation, and an in-flight embedding job (and its progress modal) all
 * survive navigating to other pages. Progress polling runs in the background
 * independent of whether ChatPage is mounted.
 */
export function ChatProvider({ children }: { children: ReactNode }) {
  const { isCreating, completedFile } = useEmbedding()
  const [messages, setMessages] = useState<ChatMessage[]>([initialMessage])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<string | null>(null)
  const [availableFiles, setAvailableFiles] = useState<string[]>([])
  const [error, setError] = useState('')
  const [hasEmbeddings, setHasEmbeddings] = useState(false)
  const abortControllerRef = useRef<AbortController | null>(null)

  // Load available CSV files once.
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
    if (!selectedFile) return
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

  const addAvailableFile = (filename: string) => {
    setAvailableFiles((prev) =>
      prev.includes(filename) ? prev : [filename, ...prev]
    )
    setSelectedFile(filename)
  }

  const stopGeneration = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    setIsLoading(false)
  }

  const sendMessage = async (customText?: string) => {
    const textToSend = (customText ?? inputMessage).trim()
    if (!textToSend || isCreating) return

    // Abort any existing in-flight request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    const controller = new AbortController()
    abortControllerRef.current = controller

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: textToSend,
      timestamp: Date.now(),
    }

    setMessages((prev) => [...prev, userMessage])
    if (!customText) {
      setInputMessage('')
    }
    setIsLoading(true)
    setError('')

    try {
      const chatRequest: ChatRequest = {
        message: textToSend,
        filename: selectedFile || undefined,
      }
      const response = await chatApi.sendMessageBody(chatRequest, controller.signal)
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: response.response,
          timestamp: Date.now(),
          sources: response.sources,
        },
      ])
    } catch (err: any) {
      // If manually stopped/cancelled by user
      if (controller.signal.aborted || err?.code === 'ERR_CANCELED' || err?.message === 'canceled') {
        setMessages((prev) => [
          ...prev,
          {
            id: (Date.now() + 1).toString(),
            type: 'assistant',
            content: '*[Generation stopped by user]*',
            timestamp: Date.now(),
          },
        ])
        return
      }

      const errMsg = err?.error || err?.detail || 'Failed to send message'
      setError(errMsg)
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: `Sorry, I encountered an error while processing your request:\n\n> ${errMsg}\n\nPlease verify that the backend is online and try again.`,
          timestamp: Date.now(),
        },
      ])
    } finally {
      if (abortControllerRef.current === controller) {
        abortControllerRef.current = null
      }
      setIsLoading(false)
    }
  }

  const regenerateResponse = async () => {
    if (isLoading || isCreating) return

    // Find the latest user message
    const lastUserMsg = [...messages].reverse().find((m) => m.type === 'user')
    if (!lastUserMsg) return

    // Remove the trailing assistant message(s) after that user message
    const userMsgIndex = messages.lastIndexOf(lastUserMsg)
    if (userMsgIndex >= 0) {
      setMessages(messages.slice(0, userMsgIndex))
    }

    await sendMessage(lastUserMsg.content)
  }

  const clearConversation = () => {
    stopGeneration()
    setMessages([
      {
        ...initialMessage,
        id: Date.now().toString(),
        timestamp: Date.now(),
      },
    ])
    setError('')
  }

  const value: ChatContextValue = {
    messages,
    inputMessage,
    setInputMessage,
    selectedFile,
    setSelectedFile,
    availableFiles,
    addAvailableFile,
    isLoading,
    error,
    setError,
    hasEmbeddings,
    sendMessage,
    stopGeneration,
    regenerateResponse,
    clearConversation,
  }

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}

export function useChat() {
  const ctx = useContext(ChatContext)
  if (!ctx) throw new Error('useChat must be used within a ChatProvider')
  return ctx
}
