import React, { createContext, useContext, useEffect, useRef, useState, useCallback } from 'react'
import { systemApi } from '@/services/api'
import type { SystemStatusResponse } from '@/types'

export type ApiStatus = 'online' | 'offline' | 'checking'
export type ModelStatus = 'loaded' | 'not_loaded' | 'loading' | 'partial' | 'error' | 'unknown' | 'checking'

interface SystemStatusContextType {
  apiStatus: ApiStatus
  modelStatus: ModelStatus
  details: SystemStatusResponse | null
  lastChecked: number | null
  refresh: () => Promise<void>
}

const SystemStatusContext = createContext<SystemStatusContextType | undefined>(undefined)

const POLL_INTERVAL_MS = 10000 // 10 seconds

export const SystemStatusProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [apiStatus, setApiStatus] = useState<ApiStatus>('checking')
  const [modelStatus, setModelStatus] = useState<ModelStatus>('checking')
  const [details, setDetails] = useState<SystemStatusResponse | null>(null)
  const [lastChecked, setLastChecked] = useState<number | null>(null)

  const abortControllerRef = useRef<AbortController | null>(null)
  const isMountedRef = useRef<boolean>(true)

  const fetchStatus = useCallback(async () => {
    // Abort previous in-flight request if still running
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    const controller = new AbortController()
    abortControllerRef.current = controller

    try {
      const data = await systemApi.getStatus(controller.signal)
      if (!isMountedRef.current) return

      if (data && data.status === 'healthy') {
        setApiStatus('online')

        // Map backend model status
        const rawModelStatus = data.models?.status?.toLowerCase()
        if (rawModelStatus === 'loaded') {
          setModelStatus('loaded')
        } else if (rawModelStatus === 'partial') {
          setModelStatus('partial')
        } else if (rawModelStatus === 'loading') {
          setModelStatus('loading')
        } else if (rawModelStatus === 'error') {
          setModelStatus('error')
        } else if (rawModelStatus === 'not_loaded') {
          setModelStatus('not_loaded')
        } else {
          setModelStatus('unknown')
        }

        setDetails(data)
        setLastChecked(Date.now())
      } else {
        setApiStatus('offline')
        setModelStatus('unknown')
        setDetails(null)
      }
    } catch (err: any) {
      if (!isMountedRef.current) return

      // Ignore abort errors
      if (err.name === 'CanceledError' || err.name === 'AbortError' || err.code === 'ERR_CANCELED') {
        return
      }

      // Backend unreachable or request timed out: API is offline, model status unknown
      setApiStatus('offline')
      setModelStatus('unknown')
      setDetails(null)
    }
  }, [])

  useEffect(() => {
    isMountedRef.current = true

    // Initial check immediately on mount
    fetchStatus()

    // Periodic polling every 10 seconds
    const intervalId = window.setInterval(() => {
      fetchStatus()
    }, POLL_INTERVAL_MS)

    return () => {
      isMountedRef.current = false
      window.clearInterval(intervalId)
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [fetchStatus])

  return (
    <SystemStatusContext.Provider
      value={{
        apiStatus,
        modelStatus,
        details,
        lastChecked,
        refresh: fetchStatus,
      }}
    >
      {children}
    </SystemStatusContext.Provider>
  )
}

export function useSystemStatus(): SystemStatusContextType {
  const context = useContext(SystemStatusContext)
  if (!context) {
    throw new Error('useSystemStatus must be used within a SystemStatusProvider')
  }
  return context
}
