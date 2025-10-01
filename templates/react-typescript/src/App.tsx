import React from 'react'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md mx-auto text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to {{PROJECT_NAME}}
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          A modern React TypeScript application
        </p>
        <button 
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          onClick={() => alert('Hello from {{PROJECT_NAME}}!')}
        >
          Get Started
        </button>
      </div>
    </div>
  )
}

export default App