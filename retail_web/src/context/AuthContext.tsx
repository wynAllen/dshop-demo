import React, { createContext, useContext, useState, useCallback } from "react";
import { getStoredToken, clearStoredToken, setStoredToken } from "../api/auth";

type AuthContextValue = {
  token: string | null;
  setToken: (t: string | null) => void;
  isLoggedIn: boolean;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setTokenState] = useState<string | null>(getStoredToken);

  const setToken = useCallback((t: string | null) => {
    if (t) setStoredToken(t);
    else clearStoredToken();
    setTokenState(t);
  }, []);

  const logout = useCallback(() => {
    clearStoredToken();
    setTokenState(null);
  }, []);

  const value: AuthContextValue = {
    token,
    setToken,
    isLoggedIn: !!token,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
