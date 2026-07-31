"use client"
import { editor } from 'monaco-editor'
import Editor, { OnMount } from '@monaco-editor/react';
import { TEditorWrapperProps } from './types';
import { useRef } from 'react';
import { removeEscapeChars } from './helpers';

export function EditorWrapper({ mutateFunc }: TEditorWrapperProps) {
    const editorRef = useRef<editor.IStandaloneCodeEditor>(null)

    const handleEditorDidMount: OnMount = (editor) => {
        editorRef.current = editor
    }

    const handleProgramSubmit = () => {
        const programString = editorRef.current?.getValue()
        if (!programString) return
        mutateFunc(removeEscapeChars(programString))
    }

    return (
        <div className='flex flex-col h-full'>
            <div className='border-2 border-amber-400 w-fit h-fit'>
                <Editor height="70vh" width="40rem" theme="vs-dark" defaultLanguage='cpp' onMount={handleEditorDidMount} />
            </div>
            <div className='flex justify-center items-center h-full'>
                <button className='text-shadow-white bg-gray-900 p-3 rounded-xl cursor-pointer' onClick={handleProgramSubmit}>Analyze code</button>
            </div>
        </div>
    )
}