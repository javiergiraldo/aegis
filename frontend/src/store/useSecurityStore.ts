import { create } from 'zustand';
import { io, Socket } from 'socket.io-client';
import { SecurityAlert } from '../types/security';

interface SecurityState {
  alerts: SecurityAlert[];
  isConnected: boolean;
  socket: Socket | null;
  connectSocket: (url: string) => void;
  disconnectSocket: () => void;
  addAlert: (alert: SecurityAlert) => void;
  clearAlerts: () => void;
}

export const useSecurityStore = create<SecurityState>((set, get) => ({
  alerts: [],
  isConnected: false,
  socket: null,

  connectSocket: (url: string) => {
    if (get().socket) return; // Prevent multiple connections

    const socket = io(url, {
      transports: ['websocket'],
      autoConnect: true,
      path: '/socket.io',
    });

    socket.on('connect', () => {
      console.log('[Socket] Connected to Aegis Telemetry Stream');
      set({ isConnected: true });
    });

    socket.on('disconnect', () => {
      console.log('[Socket] Disconnected from stream');
      set({ isConnected: false });
    });

    socket.on('security_alert', (alert: SecurityAlert) => {
      get().addAlert(alert);
    });

    set({ socket });
  },

  disconnectSocket: () => {
    const { socket } = get();
    if (socket) {
      socket.disconnect();
      set({ socket: null, isConnected: false });
    }
  },

  addAlert: (alert: SecurityAlert) => {
    set((state) => ({
      // Store the latest 100 alerts in state to avoid memory bloat
      alerts: [alert, ...state.alerts].slice(0, 100),
    }));
  },

  clearAlerts: () => {
    set({ alerts: [] });
  },
}));
