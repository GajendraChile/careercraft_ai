import { ChatInput } from "@/components/custom/chatinput";
import { PreviewMessage} from "../../components/custom/message";
import { useScrollToBottom } from '@/components/custom/use-scroll-to-bottom';
import { useState} from "react";
import { message } from "../../interfaces/interfaces"
import { Overview } from "@/components/custom/overview";
import { Header } from "@/components/custom/header";
import {v4 as uuidv4} from 'uuid';
import { searchProfiles } from "../../services/service"
import { toast } from "sonner";

//const socket = new WebSocket("ws://localhost:8090"); //change to your websocket endpoint

// get the device (instance)'s websocket endpoint
// const proto = window.location.protocol === "https:" ? "wss" : "ws";
// const host = window.location.hostname;
// const socket = new WebSocket(`${proto}://${host}:8090`);

export function Chat() {
  const [messagesContainerRef, messagesEndRef] = useScrollToBottom<HTMLDivElement>();
  const [messages, setMessages] = useState<message[]>([]);
  const [question, setQuestion] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [fileList, setFileList] = useState<any[]>([])


  // const messageHandlerRef = useRef<((event: MessageEvent) => void) | null>(null);

  // const cleanupMessageHandler = () => {
  //   if (messageHandlerRef.current && socket) {
  //     socket.removeEventListener("message", messageHandlerRef.current);
  //     messageHandlerRef.current = null;
  //   }
  // };

  function handleFileChange(event: any): void {
      setFileList([])
      let inputFiles = []
      for (let file of event?.target?.files) {
          inputFiles.push(file);
      }
      setFileList(inputFiles)
  }

  function clearUploads(): void {
      setFileList([])
  }

async function handleSubmit(text?: string) {
  //if (!socket || socket.readyState !== WebSocket.OPEN || isLoading) return;
  
  // toast("Event has been created.")
  // return

  if (fileList.length == 0){
    toast("Please upload JD pdf file.")
    return
  }

  if (!text){
    toast("Please provide input prompt along with JD.")
    return
  }
  let formData = new FormData();
  formData.append("user_query", text!);
  formData.append("file", fileList[0])
  // for (let file of fileList) {
  //   formData.append("file", file)
  // }
  setIsLoading(true);
  let response :any = await searchProfiles(formData)
  console.log(response)


  const messageText = text || question;
  // setIsLoading(true);
  // cleanupMessageHandler();
  
  const traceId = uuidv4();
  setMessages(prev => [...prev, { content: messageText, role: "user", id: traceId }]);
  // socket.send(messageText);
  setQuestion("");

  try {
    // const messageHandler = (event: MessageEvent) => {
      setIsLoading(false);
      // if(event.data.includes("[END]")) {
      //   return;
      // }
      
      setMessages(prev => {
        const lastMessage = prev[prev.length - 1];
        const newContent = lastMessage?.role === "assistant" 
          ? lastMessage.content + response["result"]
          : response["result"];
        
        const newMessage = { content: newContent, role: "assistant", id: traceId };
        return lastMessage?.role === "assistant"
          ? [...prev.slice(0, -1), newMessage]
          : [...prev, newMessage];
      });

      // if (event.data.includes("[END]")) {
      //   // cleanupMessageHandler();
      // }
    // };

    // messageHandlerRef.current = messageHandler;
    // socket.addEventListener("message", messageHandler);
  } catch (error) {
    console.error("WebSocket error:", error);
    setIsLoading(false);
  }
}

  return (
    <div className="flex flex-col min-w-0 h-dvh bg-background">
      <Header/>
      <div className="flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4" ref={messagesContainerRef}>
        {messages.length == 0 && <Overview />}
        {messages.map((message, index) => (
          <PreviewMessage key={index} message={message} />
        ))}
        {isLoading && <div className="chatbot-thinking">
          <span></span>
          <span></span>
          <span></span>
        </div>}
        <div ref={messagesEndRef} className="shrink-0 min-w-[24px] min-h-[24px]"/>
      </div>
      <div className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
        <ChatInput  
          question={question}
          setQuestion={setQuestion}
          onHandleFileChange={handleFileChange}
          clearUploadedFiles={clearUploads}
          onSubmit={handleSubmit}
          isLoading={isLoading}
          fileList={fileList}
        />
      </div>
    </div>
  );
};
