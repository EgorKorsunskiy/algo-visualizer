"use client"
import { editor } from 'monaco-editor'
import Editor, { OnMount } from '@monaco-editor/react';
import { TEditorWrapperProps } from './types';
import { useRef } from 'react';
import { removeEscapeChars } from './helpers';
import { RECORD_TYPE } from '@/visualizer/types';
import { CommandEntryWrapper, HintEntryWrapper } from '../Log';

export function EditorWrapper({ logEntries, mutateFunc }: TEditorWrapperProps) {
    const editorRef = useRef<editor.IStandaloneCodeEditor>(null)

    const handleEditorDidMount: OnMount = (editor) => {
        editorRef.current = editor
    }

    const handleProgramSubmit = () => {
        const programString = editorRef.current?.getValue()
        if (!programString) return
        mutateFunc(removeEscapeChars(programString))
    }

    const logComponents = () => {
        return logEntries.map((entry, indx) => {
            if (entry.recordType === RECORD_TYPE.COMMAND) {
                return <CommandEntryWrapper key={indx} {...entry} />
            }
            return <HintEntryWrapper key={indx} {...entry} />
        })
    }

    return (
        <div className='flex flex-col h-full gap-4'>
            <div className='border-2 border-amber-400 w-fit h-fit'>
                <Editor height="70vh" width="40rem" theme="vs-dark" defaultLanguage='cpp' onMount={handleEditorDidMount} />
            </div>
            <div className='flex justify-center items-start'>
                <button className='text-shadow-white bg-gray-900 p-3 rounded-xl cursor-pointer' onClick={handleProgramSubmit}>Analyze code</button>
            </div>
            {logEntries.length > 0 && (
                <div className='flex flex-col gap-4 max-h-60 overflow-scroll p-4'>
                    {logComponents()}
                </div>
            )}
        </div>
    )
}