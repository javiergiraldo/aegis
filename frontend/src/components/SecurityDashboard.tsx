import React, { useEffect } from 'react';
import { useSecurityStore } from '../store/useSecurityStore';

const severityColors: Record<string, string> = {
  INFO: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  WARNING: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  CRITICAL: 'bg-red-500/10 text-red-400 border-red-500/20'
};

export const SecurityDashboard: React.FC = () => {
  const { alerts, isConnected, connectSocket, disconnectSocket } = useSecurityStore();

  useEffect(() => {
    // Configuración del WebSocket al puerto local de FastAPI (en producción sería dinámico)
    connectSocket('http://localhost:8000');
    return () => {
      disconnectSocket();
    };
  }, [connectSocket, disconnectSocket]);

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-gray-100 p-8 font-mono">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Cabecera Principal */}
        <header className="flex justify-between items-center border-b border-green-900/50 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tighter text-green-500 drop-shadow-[0_0_10px_rgba(34,197,94,0.5)]">
              &gt; Aegis Security Posture
            </h1>
            <p className="text-gray-400 text-sm mt-2">Zero-Trust Real-Time Telemetry Stream</p>
          </div>
          
          {/* Indicador de Estado del WebSocket */}
          <div className="flex items-center gap-3 bg-black/50 px-5 py-2.5 rounded-lg border border-gray-800 shadow-[0_0_15px_rgba(0,0,0,0.5)]">
            <span className="text-sm text-gray-400">STATUS:</span>
            {isConnected ? (
              <span className="flex items-center gap-2 text-green-400 text-sm font-semibold tracking-widest">
                <span className="relative flex h-3 w-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500 drop-shadow-[0_0_8px_rgba(34,197,94,1)]"></span>
                </span>
                ONLINE
              </span>
            ) : (
              <span className="flex items-center gap-2 text-red-500 text-sm font-semibold tracking-widest">
                <div className="w-3 h-3 bg-red-600 rounded-full drop-shadow-[0_0_8px_rgba(220,38,38,1)]"></div>
                OFFLINE
              </span>
            )}
          </div>
        </header>

        {/* Panel de Datos / Tabla */}
        <div className="bg-[#111] rounded-xl border border-gray-800/80 overflow-hidden shadow-2xl backdrop-blur-sm">
          <div className="px-6 py-4 border-b border-gray-800/80 bg-[#0f0f0f]">
            <h2 className="text-lg font-semibold text-gray-300">Live Intrusion Feed</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-black/30 text-gray-500 text-xs uppercase tracking-widest border-b border-gray-800/50">
                  <th className="p-4 font-medium">Timestamp</th>
                  <th className="p-4 font-medium">Severity</th>
                  <th className="p-4 font-medium">Alert Type</th>
                  <th className="p-4 font-medium">Source IP</th>
                  <th className="p-4 font-medium">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/30">
                {alerts.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="p-12 text-center text-gray-600 italic">
                      <span className="animate-pulse">Awaiting incoming telemetry streams...</span>
                    </td>
                  </tr>
                ) : (
                  alerts.map((alert) => (
                    <tr key={alert.id} className="hover:bg-gray-800/20 transition-all duration-200">
                      <td className="p-4 text-gray-400 text-xs">
                        {new Date(alert.timestamp).toLocaleTimeString()}
                      </td>
                      <td className="p-4">
                        <span className={`px-3 py-1 rounded border text-xs font-bold tracking-wide shadow-sm ${severityColors[alert.severity]}`}>
                          {alert.severity}
                        </span>
                      </td>
                      <td className="p-4 font-semibold text-gray-300 text-sm">
                        {alert.alert_type}
                      </td>
                      <td className="p-4">
                        <span className="bg-black text-gray-400 px-2.5 py-1 rounded border border-gray-700/50 text-xs font-mono select-all">
                          {alert.source_ip}
                        </span>
                      </td>
                      <td className="p-4 text-gray-400 text-sm truncate max-w-xs">
                        {alert.description}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
