export const translations = {
    en: { dashboard: "Dashboard", generate: "Generate Report", library: "Chart Library" },
    "zh-TW": { dashboard: "儀表板", generate: "產生報告", library: "命盤庫" },
    "zh-CN": { dashboard: "仪表板", generate: "生成报告", library: "命盘库" },
    ja: { dashboard: "ダッシュボード", generate: "レポート作成", library: "チャートライブラリ" }
};

export const getTranslation = (lang: keyof typeof translations, key: keyof typeof translations['en']) => {
    return translations[lang]?.[key] || translations['en'][key];
};
