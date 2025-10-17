import { Textarea } from "../ui/textarea";
import { cx } from 'classix';
import { Button } from "../ui/button";
import { ArrowUpIcon, TrashIcon, UploadIcon, } from "./icons"
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import {useRef, useState } from 'react';

interface ChatInputProps {
    question: string;
    setQuestion: (question: string) => void;
    onHandleFileChange: (event?: any) => void;
    clearUploadedFiles: () => void;
    onSubmit: (text?: string) => void;
    isLoading: boolean;
    fileList: File[]
}

const suggestedActions = [
    {
        title: 'Can you suggest profiles for angular + python',
        label: 'for skoda?',
        action: 'Can you suggest profiles for angular + python for skoda?',
    },
    {
        title: 'Can you suggest someone with aws experience',
        label: 'for palCo?',
        action: 'Can you suggest someone with aws experience for palCo?',
    },
];

export const ChatInput = ({ question, setQuestion, onHandleFileChange, clearUploadedFiles, onSubmit, isLoading , fileList }: ChatInputProps) => {
    const [showSuggestions, setShowSuggestions] = useState(true);
    const fileInputRef = useRef<any>(null);

    return(
    <div className="relative w-full flex flex-col gap-4">
        {showSuggestions && (
            <div className="hidden md:grid sm:grid-cols-2 gap-2 w-full">
                {suggestedActions.map((suggestedAction, index) => (
                    <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 20 }}
                    transition={{ delay: 0.05 * index }}
                    key={index}
                    className={index > 1 ? 'hidden sm:block' : 'block'}
                    >
                        <Button
                            variant="ghost"
                            onClick={ () => {
                                const text = suggestedAction.action;
                                onSubmit(text);
                                setShowSuggestions(false);
                            }}
                            className="text-left border rounded-xl px-4 py-3.5 text-sm flex-1 gap-1 sm:flex-col w-full h-auto justify-start items-start"
                        >
                            <span className="font-medium">{suggestedAction.title}</span>
                            <span className="text-muted-foreground">
                            {suggestedAction.label}
                            </span>
                        </Button>
                    </motion.div>
                ))}
            </div>
        )}
        <input
        type="file"
        className="fixed -top-4 -left-4 size-0.5 opacity-0 pointer-events-none"
        multiple
        tabIndex={-1}
        />

        {fileList.length > 0 && (
            <div className="bg-muted rounded-xl p-3 text-sm text-muted-foreground mb-2">
                <strong>Uploaded file:</strong> {fileList.map((file, idx) => (
                <div key={idx}>{file.name}</div>
                ))}
            </div>
        )}


        <Textarea
        placeholder="Please Upload the JD pdf file here to find matching candidate profiles."
        className={cx(
            'min-h-[24px] max-h-[calc(75dvh)] overflow-hidden resize-none rounded-xl text-base bg-muted',
        )}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();

                if (isLoading) {
                    toast.error('Please wait for the model to finish its response!');
                } else {
                    setShowSuggestions(false);
                    onSubmit();
                }
            }
        }}
        rows={3}
        autoFocus
        />

        <Button 
            className="rounded-full p-1.5 h-fit absolute bottom-2 right-2 m-0.5 border dark:border-zinc-600"
            onClick={() => {setShowSuggestions(false);onSubmit(question)}}
            disabled={question.length === 0 || isLoading}
        >
            <ArrowUpIcon size={14} />
        </Button>
        <input
            type="file"
            ref={fileInputRef} // Create a ref to access this element
            style={{ display: 'none' }}
            onChange={onHandleFileChange} // Handle file selection
        />

        <Button 
            className="rounded-full p-1.5 h-fit absolute bottom-2 left-10 m-0.5 border dark:border-zinc-600"
            onClick={() => clearUploadedFiles()}
            disabled={isLoading}
        >
            <TrashIcon size={14} />
        </Button>

        <Button 
            className="rounded-full p-1.5 h-fit absolute bottom-2 left-2 m-0.5 border dark:border-zinc-600"
            onClick={() => {fileInputRef?.current?.click()}}
            disabled={isLoading}
        >
            <UploadIcon size={14} />
        </Button>

    </div>
    );
}