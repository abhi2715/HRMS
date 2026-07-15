/**
 * Zustand auth store — manages authentication state.
 */

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone: string | null;
  avatar_url: string | null;
  primary_role: string;
  is_active: boolean;
  is_verified: boolean;
  last_login: string | null;
  created_at: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  setAuth: (user: User, accessToken: string, refreshToken: string) => void;
  setUser: (user: User) => void;
  setLoading: (loading: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: {
        id: "238dd245-8d10-4b34-8b12-ec1b9b38b45b",
        email: "rajesh.kumar@hrcopilot.io",
        first_name: "Rajesh",
        last_name: "Kumar",
        full_name: "Rajesh Kumar",
        phone: null,
        avatar_url: null,
        primary_role: "SUPER_ADMIN",
        is_active: true,
        is_verified: true,
        last_login: new Date().toISOString(),
        created_at: new Date().toISOString(),
      },
      accessToken: "fake-access-token",
      refreshToken: "fake-refresh-token",
      isAuthenticated: true,
      isLoading: false,

      setAuth: (user, accessToken, refreshToken) => {
        if (typeof window !== "undefined") {
          localStorage.setItem("access_token", accessToken);
          localStorage.setItem("refresh_token", refreshToken);
        }
        set({
          user,
          accessToken,
          refreshToken,
          isAuthenticated: true,
          isLoading: false,
        });
      },

      setUser: (user) => set({ user }),

      setLoading: (isLoading) => set({ isLoading }),

      logout: () => {
        if (typeof window !== "undefined") {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
        }
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
          isLoading: false,
        });
      },
    }),
    {
      name: "hrms-auth",
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
