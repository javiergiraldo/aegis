export interface SecurityAlert {
  id: string;
  source_ip: string;
  severity: 'INFO' | 'WARNING' | 'CRITICAL';
  alert_type: string;
  description: string;
  created_at: string;
  payload?: Record<string, any>;
}
