module.exports = [
"[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// ChatInterface.tsx
// Component for the Marriage EQ OS chat interface.
// Dependencies: React, Tailwind CSS
// This component handles message display, input, module selection, and local storage.
__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
;
;
const modulePrompts = {
    'Base': "You are my Personal Life OS with a specialized focus on emotional intelligence, marriage health, and Catholic virtue development...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
    'Morning Kickstart': "MORNING KICKSTART MODE ACTIVATED\n\nYour job: Help me start the day with clarity, presence, and wife-focused awareness...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
    'Crisis Support': "CRISIS MODE ACTIVATED\n\nYou've indicated: Wife is upset / I messed up / Conflict happening...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
    'Risk Audit': "WEEKLY RISK AUDIT (Through Her Lens)\n\nThis is a *security assessment* from your wife's perspective...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
    'Pattern Spotter': "WEEKLY PATTERN ANALYSIS\n\nAnswer these questions honestly. I'll help you see what you're missing...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)",
    'Mini Journal': "EVENING CHECK-IN (3 minutes)\n\nQuick daily capture...\n\n(See marriage_EQ_OS_2025-11-14.md for full prompt)"
};
const ChatInterface = ()=>{
    const [messages, setMessages] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])([]);
    const [currentModule, setCurrentModule] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])('Base');
    const [newMessage, setNewMessage] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])('');
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        // Load chat history from local storage
        const storedMessages = localStorage.getItem('chatMessages');
        if (storedMessages) {
            setMessages(JSON.parse(storedMessages));
        }
        // Load selected module from local storage
        const storedModule = localStorage.getItem('selectedModule');
        if (storedModule) {
            setCurrentModule(storedModule);
        }
        // Add system message based on selected module
        const systemMessage = modulePrompts[currentModule] || 'Base Prompt';
        setMessages([
            ...messages,
            `System: ${systemMessage}`
        ]);
    }, [
        currentModule,
        messages
    ]);
    const handleModuleChange = (event)=>{
        const selectedModule = event.target.value;
        setCurrentModule(selectedModule);
        localStorage.setItem('selectedModule', selectedModule);
        // Add system message when module changes
        const systemMessage = modulePrompts[selectedModule] || 'Base Prompt';
        setMessages([
            ...messages,
            `System: ${systemMessage}`
        ]);
    };
    const handleSendMessage = async ()=>{
        if (newMessage.trim() !== '') {
            setMessages([
                ...messages,
                `User: ${newMessage}`
            ]);
            setNewMessage('');
            try {
                const response = await fetch('https://api.anthropic.com/v1/messages', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${process.env.CLAUDE_API_KEY}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        model: 'claude-3-opus-20240229',
                        max_tokens: 200,
                        messages: [
                            {
                                'role': 'user',
                                'content': newMessage
                            }
                        ]
                    })
                });
                const data = await response.json();
                const aiResponse = data.choices[0].message.content;
                setMessages([
                    ...messages,
                    `User: ${newMessage}`,
                    `AI: ${aiResponse}`
                ]);
                // Simplified SPR Compression: Extract key insights and recommendations
                const sprSummary = `Key Insights: ${messages.slice(-5).map((msg)=>msg.split(':')[1]).join(', ')}\nRecommendations: Based on recent conversation, consider...`;
                localStorage.setItem('chatMessages', JSON.stringify({
                    summary: sprSummary,
                    fullMessages: [
                        ...messages,
                        `User: ${newMessage}`,
                        `AI: ${aiResponse}`
                    ]
                }));
            } catch (error) {
                console.error('Error calling Claude API:', error);
                setMessages([
                    ...messages,
                    `User: ${newMessage}`,
                    `AI: Error generating response`
                ]);
                localStorage.setItem('chatMessages', JSON.stringify([
                    ...messages,
                    `User: ${newMessage}`,
                    `AI: Error generating response`
                ]));
            }
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex flex-col h-full bg-gray-800 text-white",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-4",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        htmlFor: "moduleSelect",
                        className: "block text-sm font-medium text-gray-300",
                        children: "Select Module:"
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                        lineNumber: 89,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                        id: "moduleSelect",
                        value: currentModule,
                        onChange: handleModuleChange,
                        className: "mt-2 block w-full rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:w-64",
                        children: Object.keys(modulePrompts).map((module)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                value: module,
                                children: module
                            }, module, false, {
                                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                                lineNumber: 97,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)))
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                        lineNumber: 90,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                lineNumber: 88,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex-1 p-4 overflow-y-auto",
                children: messages.map((message, index)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mb-2",
                        children: message
                    }, index, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                        lineNumber: 105,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)))
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                lineNumber: 103,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "p-4",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                        type: "text",
                        value: newMessage,
                        onChange: (e)=>setNewMessage(e.target.value),
                        className: "flex-1 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 w-full mr-2",
                        placeholder: "Type your message..."
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                        lineNumber: 113,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: handleSendMessage,
                        className: "bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-md",
                        children: "Send"
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                        lineNumber: 120,
                        columnNumber: 9
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
                lineNumber: 112,
                columnNumber: 7
            }, ("TURBOPACK compile-time value", void 0))
        ]
    }, void 0, true, {
        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx",
        lineNumber: 86,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
const __TURBOPACK__default__export__ = ChatInterface;
}),
"[project]/Documents/LifeOS/01-Projects/Development/app/chat/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// app/chat/page.tsx
__turbopack_context__.s([
    "default",
    ()=>ChatPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$app$2f$components$2f$ChatInterface$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/app/components/ChatInterface.tsx [app-ssr] (ecmascript)");
'use client';
;
;
function ChatPage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                children: "Chat"
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/chat/page.tsx",
                lineNumber: 10,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$app$2f$components$2f$ChatInterface$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {}, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/chat/page.tsx",
                lineNumber: 11,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/chat/page.tsx",
        lineNumber: 9,
        columnNumber: 5
    }, this);
}
}),
"[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

module.exports = __turbopack_context__.r("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)").vendored['react-ssr'].ReactJsxDevRuntime; //# sourceMappingURL=react-jsx-dev-runtime.js.map
}),
];

//# sourceMappingURL=Documents_LifeOS_01-Projects_Development_8e495a03._.js.map