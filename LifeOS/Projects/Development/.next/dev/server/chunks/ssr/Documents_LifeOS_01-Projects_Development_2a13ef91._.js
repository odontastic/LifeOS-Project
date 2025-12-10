module.exports = [
"[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// JournalView.tsx
// Component for displaying daily journal entries with navigation and export options.
__turbopack_context__.s([
    "default",
    ()=>JournalView
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
'use client';
;
;
function JournalView() {
    const [journals, setJournals] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({});
    const [currentDate, setCurrentDate] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(new Date().toISOString().split('T')[0]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const saved = localStorage.getItem('marriageEqJournals');
        if (saved) setJournals(JSON.parse(saved));
    }, []);
    const currentEntry = journals[currentDate] || {};
    const exportData = (format)=>{
        let content = '';
        if (format === 'json') {
            content = JSON.stringify(journals, null, 2);
        } else if (format === 'markdown') {
            content = Object.entries(journals).map(([date, entry])=>{
                return `# ${date}\n\n${entry.chatSessions?.map((s)=>s.messages.map((m)=>`**${m.role}:** ${m.content}`).join('\n')).join('\n\n') || ''}`;
            }).join('\n\n---\n\n');
        }
        const blob = new Blob([
            content
        ], {
            type: 'text/plain'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `journal.${format}`;
        a.click();
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "p-4 max-w-4xl mx-auto",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                className: "text-2xl font-bold mb-6",
                children: "Daily Journal"
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                lineNumber: 38,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                    type: "date",
                    value: currentDate,
                    onChange: (e)=>setCurrentDate(e.target.value),
                    className: "p-2 border rounded"
                }, void 0, false, {
                    fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                    lineNumber: 40,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                lineNumber: 39,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-6",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                        className: "text-xl font-semibold mb-2",
                        children: currentDate
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                        lineNumber: 48,
                        columnNumber: 9
                    }, this),
                    currentEntry.chatSessions ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        children: currentEntry.chatSessions.map((session, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "mb-4 p-4 border rounded",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                                        className: "font-semibold",
                                        children: session.module
                                    }, void 0, false, {
                                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                                        lineNumber: 53,
                                        columnNumber: 17
                                    }, this),
                                    session.messages.map((msg, j)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "mb-2",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                                                    children: [
                                                        msg.role,
                                                        ":"
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                                                    lineNumber: 56,
                                                    columnNumber: 21
                                                }, this),
                                                " ",
                                                msg.spr || msg.content
                                            ]
                                        }, j, true, {
                                            fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                                            lineNumber: 55,
                                            columnNumber: 19
                                        }, this))
                                ]
                            }, i, true, {
                                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                                lineNumber: 52,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                        lineNumber: 50,
                        columnNumber: 11
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        children: "No entries for this date."
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                        lineNumber: 63,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                lineNumber: 47,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>exportData('json'),
                        className: "px-4 py-2 bg-blue-500 text-white rounded mr-2",
                        children: "Export JSON"
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                        lineNumber: 67,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>exportData('markdown'),
                        className: "px-4 py-2 bg-green-500 text-white rounded mr-2",
                        children: "Export Markdown"
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                        lineNumber: 70,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: ()=>exportData('csv'),
                        className: "px-4 py-2 bg-purple-500 text-white rounded",
                        children: "Export CSV"
                    }, void 0, false, {
                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                        lineNumber: 73,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
                lineNumber: 66,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx",
        lineNumber: 37,
        columnNumber: 5
    }, this);
}
}),
"[project]/Documents/LifeOS/01-Projects/Development/app/journal/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// app/journal/page.tsx
__turbopack_context__.s([
    "default",
    ()=>JournalPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$app$2f$components$2f$JournalView$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/app/components/JournalView.tsx [app-ssr] (ecmascript)");
'use client';
;
;
function JournalPage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                children: "Journal"
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/journal/page.tsx",
                lineNumber: 10,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$app$2f$components$2f$JournalView$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {}, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/journal/page.tsx",
                lineNumber: 11,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/journal/page.tsx",
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

//# sourceMappingURL=Documents_LifeOS_01-Projects_Development_2a13ef91._.js.map