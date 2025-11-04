import React, { useState, useRef } from "react";
import axios from "axios";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [lastConvId, setLastConvId] = useState(null);
  const [graphJson, setGraphJson] = useState(null);
  const [showGraph, setShowGraph] = useState(false);

  // 🧠 Handle send text message
  const handleSend = async (text = input) => {
    if (!text.trim()) return;
    const userMessage = { sender: "user", text };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post("/api/v1/chat/query", {
        user_id: 1,
        text,
        conv_id: lastConvId, // continue conversation if available
      });
      const botMessage = {
        sender: "bot",
        text: response.data.answer || "No reply",
      };
      setMessages((prev) => [...prev, botMessage]);
      if (response.data.conv_id) setLastConvId(response.data.conv_id);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error: unable to fetch response" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // 🎙 Voice recording
  const handleVoice = async () => {
    if (recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      setAudioChunks([]);
      setRecording(true);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) setAudioChunks((prev) => [...prev, e.data]);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("file", audioBlob, "voice.webm");

        try {
          const res = await axios.post("/api/v1/voice", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
          if (res.data.text) await handleSend(res.data.text);
        } catch (err) {
          console.error(err);
          setMessages((prev) => [
            ...prev,
            { sender: "bot", text: "Voice processing failed." },
          ]);
        }
      };

      mediaRecorder.start();
    } catch (err) {
      console.error(err);
      alert("Microphone access denied or unavailable.");
    }
  };

  // 📄 OCR upload
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("/api/v1/ocr", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      if (res.data.text) await handleSend(res.data.text);
    } catch (err) {
      console.error(err);
      alert("OCR failed to process image");
    }
  };

  // 🧩 Fetch LangGraph reasoning graph
  const handleShowGraph = async () => {
    if (!lastConvId) {
      alert("No conversation id available. Send a message first.");
      return;
    }
    try {
      const res = await axios.get(`/api/v1/graph/${lastConvId}`);
      setGraphJson(res.data);
      setShowGraph(true);
    } catch (err) {
      console.error(err);
      alert("Graph fetch failed");
    }
  };

  return (
    <div className="chat-container" style={{ maxWidth: 700, margin: "0 auto", padding: 20 }}>
      <h2 style={{ textAlign: "center", marginBottom: 10 }}>🧬 GenAI Medical Chatbot</h2>

      <div
        className="chat-box"
        style={{
          border: "1px solid #ccc",
          borderRadius: 8,
          padding: 10,
          height: 400,
          overflowY: "auto",
          background: "#f9f9f9",
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              margin: "8px 0",
              textAlign: msg.sender === "user" ? "right" : "left",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 12,
                background: msg.sender === "user" ? "#d1e7ff" : "#e2e2e2",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
        {loading && <div className="chat-message bot">Thinking...</div>}
      </div>

      {/* Input bar */}
      <div
        className="input-area"
        style={{ display: "flex", gap: 8, marginTop: 10 }}
      >
        <input
          type="text"
          value={input}
          placeholder="Ask a medical question..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          style={{
            flex: 1,
            padding: "8px 10px",
            borderRadius: 8,
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={() => handleSend()}
          style={{
            background: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: 8,
            padding: "8px 14px",
          }}
        >
          Send
        </button>
      </div>

      {/* Controls */}
      <div
        className="voice-ocr-controls"
        style={{ marginTop: 10, display: "flex", gap: 10 }}
      >
        <button
          onClick={handleVoice}
          style={{
            background: recording ? "#dc3545" : "#198754",
            color: "#fff",
            border: "none",
            borderRadius: 8,
            padding: "8px 14px",
          }}
        >
          {recording ? "⏹ Stop" : "🎙 Voice"}
        </button>

        <input
          type="file"
          accept="image/*"
          id="ocrInput"
          style={{ display: "none" }}
          onChange={handleFileUpload}
        />
        <label
          htmlFor="ocrInput"
          className="ocr-label"
          style={{
            background: "#ffc107",
            padding: "8px 14px",
            borderRadius: 8,
            cursor: "pointer",
          }}
        >
          📄 Upload
        </label>

        <button
          onClick={handleShowGraph}
          style={{
            background: "#6f42c1",
            color: "#fff",
            border: "none",
            borderRadius: 8,
            padding: "8px 14px",
          }}
        >
          🧠 Show Reasoning Graph
        </button>
      </div>

      {/* Graph Modal */}
      {showGraph && (
        <div
          className="graph-modal"
          style={{
            position: "fixed",
            right: 20,
            top: 70,
            width: 480,
            height: 400,
            overflow: "auto",
            background: "#fff",
            padding: 12,
            borderRadius: 8,
            boxShadow: "0 6px 20px rgba(0,0,0,0.2)",
            zIndex: 10,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: 6,
            }}
          >
            <strong>Reasoning Graph (conv: {lastConvId})</strong>
            <button onClick={() => setShowGraph(false)}>Close</button>
          </div>
          <pre style={{ fontSize: 12 }}>{JSON.stringify(graphJson, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
