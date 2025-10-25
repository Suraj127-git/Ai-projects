import React, { useState, useRef } from "react";
import axios from "axios";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const [audioChunks, setAudioChunks] = useState([]);

  const handleSend = async (text = input) => {
    if (!text.trim()) return;
    const userMessage = { sender: "user", text };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post("/api/v1/chat", { message: text });
      const botMessage = {
        sender: "bot",
        text: response.data.response || "No reply",
      };
      setMessages((prev) => [...prev, botMessage]);
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

  // 🎙 Voice Recording
  const handleVoice = async () => {
    if (recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      return;
    }

    setAudioChunks([]);
    setRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder;

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
        handleSend(res.data.text);
      } catch (err) {
        console.error(err);
      }
    };

    mediaRecorder.start();
  };

  // 📄 OCR Upload
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("/api/v1/ocr", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      handleSend(res.data.text);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            <span>{msg.text}</span>
          </div>
        ))}
        {loading && <div className="chat-message bot">Thinking...</div>}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          placeholder="Ask a medical question..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={() => handleSend()}>Send</button>
      </div>

      <div className="voice-ocr-controls">
        <button onClick={handleVoice}>
          {recording ? "⏹ Stop" : "🎙 Voice"}
        </button>

        <input
          type="file"
          accept="image/*"
          id="ocrInput"
          style={{ display: "none" }}
          onChange={handleFileUpload}
        />
        <label htmlFor="ocrInput" className="ocr-label">
          📄 Upload
        </label>
      </div>
    </div>
  );
}
