module.exports = [
"[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// RiskAudit.tsx
// Interactive component for weekly risk audit with 5 categories × 7 days grid, scoring, and AI analysis.
__turbopack_context__.s([
    "default",
    ()=>RiskAudit
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
'use client';
;
;
const categories = [
    'Physical Security',
    'Household Reliability',
    'Parenting Example',
    'Emotional Attunement',
    'Follow-Through'
];
function RiskAudit() {
    const [audit, setAudit] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({});
    const [score, setScore] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(0);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const saved = localStorage.getItem('marriageEqRiskAudit');
        if (saved) setAudit(JSON.parse(saved));
    }, []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const total = Object.values(audit).filter((v)=>v === '✓').length;
        setScore(total);
    }, [
        audit
    ]);
    const toggleValue = (category, day)=>{
        const key = `${category}-${day}`;
        const current = audit[key] || '';
        const next = current === '' ? '✓' : current === '✓' ? '~' : current === '~' ? '✗' : '';
        setAudit({
            ...audit,
            [key]: next
        });
        localStorage.setItem('marriageEqRiskAudit', JSON.stringify({
            ...audit,
            [key]: next
        }));
    };
    const getColor = ()=>{
        if (score >= 20) return 'text-green-600';
        if (score >= 10) return 'text-yellow-600';
        return 'text-red-600';
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "p-4 max-w-4xl mx-auto",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                className: "text-2xl font-bold mb-6",
                children: "Weekly Risk Audit"
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                lineNumber: 40,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-4",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    className: `text-lg font-semibold ${getColor()}`,
                    children: [
                        "Score: ",
                        score,
                        "/35 ✓ marks"
                    ]
                }, void 0, true, {
                    fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                    lineNumber: 42,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                lineNumber: 41,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "overflow-x-auto",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("table", {
                    className: "w-full border-collapse border",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("thead", {
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                        className: "border p-2",
                                        children: "Category"
                                    }, void 0, false, {
                                        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                                        lineNumber: 50,
                                        columnNumber: 15
                                    }, this),
                                    Array.from({
                                        length: 7
                                    }, (_, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                            className: "border p-2",
                                            children: [
                                                "Day ",
                                                i + 1
                                            ]
                                        }, i, true, {
                                            fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                                            lineNumber: 52,
                                            columnNumber: 17
                                        }, this))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                                lineNumber: 49,
                                columnNumber: 13
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                            lineNumber: 48,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("tbody", {
                            children: categories.map((category)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                            className: "border p-2 font-semibold",
                                            children: category
                                        }, void 0, false, {
                                            fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                                            lineNumber: 59,
                                            columnNumber: 17
                                        }, this),
                                        Array.from({
                                            length: 7
                                        }, (_, day)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                                className: "border p-2 text-center",
                                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                    onClick: ()=>toggleValue(category, day),
                                                    className: "w-8 h-8 border rounded hover:bg-gray-100",
                                                    children: audit[`${category}-${day}`] || ''
                                                }, void 0, false, {
                                                    fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                                                    lineNumber: 62,
                                                    columnNumber: 21
                                                }, this)
                                            }, day, false, {
                                                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                                                lineNumber: 61,
                                                columnNumber: 19
                                            }, this))
                                    ]
                                }, category, true, {
                                    fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                                    lineNumber: 58,
                                    columnNumber: 15
                                }, this))
                        }, void 0, false, {
                            fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                            lineNumber: 56,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                    lineNumber: 47,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                lineNumber: 46,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-6",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                    className: "px-4 py-2 bg-blue-500 text-white rounded",
                    children: "AI Analysis (Placeholder)"
                }, void 0, false, {
                    fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                    lineNumber: 76,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
                lineNumber: 75,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx",
        lineNumber: 39,
        columnNumber: 5
    }, this);
}
}),
"[project]/Documents/LifeOS/01-Projects/Development/app/risk-audit/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// app/risk-audit/page.tsx
__turbopack_context__.s([
    "default",
    ()=>RiskAuditPage
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$app$2f$components$2f$RiskAudit$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Documents/LifeOS/01-Projects/Development/app/components/RiskAudit.tsx [app-ssr] (ecmascript)");
'use client';
;
;
function RiskAuditPage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                children: "Risk Audit"
            }, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/risk-audit/page.tsx",
                lineNumber: 10,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Documents$2f$LifeOS$2f$01$2d$Projects$2f$Development$2f$app$2f$components$2f$RiskAudit$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {}, void 0, false, {
                fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/risk-audit/page.tsx",
                lineNumber: 11,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Documents/LifeOS/01-Projects/Development/app/risk-audit/page.tsx",
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

//# sourceMappingURL=Documents_LifeOS_01-Projects_Development_1463bbab._.js.map