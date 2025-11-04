import React, { useState } from 'react';
import { AuthProvider, useAuth, LoginForm, RegisterForm } from '@genai-med-chat/auth';
import { Chat } from '@genai-med-chat/chat';
import { Button } from '@genai-med-chat/shared';

const App = () => {
  return (
    <AuthProvider>
      <Main />
    </AuthProvider>
  );
};

const Main = () => {
  const { user, logout } = useAuth();
  const [isRegistering, setIsRegistering] = useState(false);

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="w-full max-w-md">
          {isRegistering ? (
            <RegisterForm 
              onRegister={async (userData) => {
                // The register function from useAuth will be called here
              }}
              onSwitchToLogin={() => setIsRegistering(false)} 
            />
          ) : (
            <LoginForm 
              onLogin={async (credentials) => {
                // The login function from useAuth will be called here
              }}
              onSwitchToRegister={() => setIsRegistering(true)} 
            />
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app h-screen flex flex-col">
      <header className="bg-white shadow-md p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">🩺 GenAI Medical Chatbot</h1>
        <Button onClick={logout} variant="secondary">Logout</Button>
      </header>
      <main className="flex-1 p-4 overflow-hidden">
        <Chat />
      </main>
    </div>
  );
};

export default App;
