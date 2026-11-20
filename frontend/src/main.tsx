import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'sonner'
import App from './App.tsx'
import './index.css'
import 'katex/dist/katex.min.css'
import 'highlight.js/styles/atom-one-dark.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster 
        position="top-right" 
        richColors 
        closeButton
        toastOptions={{
          duration: 4000,
        }}
      />
    </BrowserRouter>
  </React.StrictMode>,
)