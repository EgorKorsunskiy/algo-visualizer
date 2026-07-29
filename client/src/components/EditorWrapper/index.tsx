"use client"
import Editor from '@monaco-editor/react';

export function EditorWrapper() {
    return (
        <div className='flex flex-col h-full'>
            <div className='border-2 border-amber-400 w-fit h-fit'>
                <Editor height="70vh" width="40rem" theme="vs-dark" defaultLanguage='cpp' />
            </div>
            <div className='flex justify-center items-center h-full'>
                <button className='text-shadow-white bg-gray-900 p-3 rounded-xl cursor-pointer'>Analyze code</button>
            </div>
        </div>
    )
}