import { create } from "zustand";

interface AppState {
  theme: "light" | "dark";
  initialized: boolean;
  error?: string;
  initialize: () => void;
  toggleTheme: () => void;
}

export const useAppState = create<AppState>((set, get) => ({
  theme: "dark",
  initialized: false,
  error: undefined,
  initialize: () => {
    try {
      set({ initialized: true });
    } catch (error) {
      set({ error: (error as Error).message });
    }
  },
  toggleTheme: () => {
    set({ theme: get().theme === "dark" ? "light" : "dark" });
  }
}));
