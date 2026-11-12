export interface ChatMessage {
  role: string;
  content: string;
  meta?: Record<string, unknown>;
}

export interface ChatResponse {
  id: string;
  choices: Array<{ message: { role: string; content: string }; finish_reason: string }>;
  usage?: Record<string, unknown>;
}

export class QHarnessClient {
  private baseUrl: string;
  private token?: string;
  private model: string;

  constructor(baseUrl = "http://127.0.0.1:8000", token?: string, model = "qharness") {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.token = token;
    this.model = model;
  }

  private headers(): Record<string, string> {
    const h: Record<string, string> = { "Content-Type": "application/json" };
    if (this.token) h["Authorization"] = `Bearer ${this.token}`;
    return h;
  }

  async chat(prompt: string, sessionId?: string): Promise<ChatResponse> {
    const body: Record<string, unknown> = {
      model: this.model,
      messages: [{ role: "user", content: prompt, meta: sessionId ? { session_id: sessionId } : {} }],
    };
    const res = await fetch(`${this.baseUrl}/v1/chat/completions`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`qharness error: ${res.status}`);
    return (await res.json()) as ChatResponse;
  }

  async health(): Promise<{ status: string }> {
    const res = await fetch(`${this.baseUrl}/health`);
    return (await res.json()) as { status: string };
  }
}
