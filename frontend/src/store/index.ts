import { create } from 'zustand';
import axios from 'axios';

export interface ChartPayload {
    year: number;
    month: number;
    day: number;
    time_branch: string;
    gender: 'M' | 'F';
}

export interface ZiweiChart {
    palaces: any[];
    [key: string]: any;
}

export interface StoreState {
    currentChart: ZiweiChart | null;
    detectedPatterns: any[] | null;
    matchRate: number | null;
    crossValidation: any | null;
    correctionSuggestion: any | null;
    isLoading: boolean;
    error: string | null;
    fetchChartAndConsensus: (payload: ChartPayload) => Promise<void>;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const API_KEY = import.meta.env.VITE_API_KEY || 'default_secure_api_key_for_testing';

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
    }
});

export const useStore = create<StoreState>((set) => ({
    currentChart: null,
    detectedPatterns: null,
    matchRate: null,
    crossValidation: null,
    correctionSuggestion: null,
    isLoading: false,
    error: null,

    fetchChartAndConsensus: async (payload: ChartPayload) => {
        set({ isLoading: true, error: null });
        try {
            const chartRes = await apiClient.post('/ziwei/chart', payload);
            const ziweiChart = chartRes.data.ziwei_chart;

            const patternRes = await apiClient.post('/ziwei/patterns', payload);
            const patterns = patternRes.data.detected_patterns;
            const matchRate = patternRes.data.match_rate;

            const consensusRes = await apiClient.post('/consensus', payload);
            const crossValidation = consensusRes.data.cross_validation;
            const correctionSuggestion = consensusRes.data.correction_suggestion;

            set({
                currentChart: ziweiChart,
                detectedPatterns: patterns,
                matchRate: matchRate,
                crossValidation: crossValidation,
                correctionSuggestion: correctionSuggestion,
                isLoading: false
            });

        } catch (error: any) {
            set({
                error: error.response?.data?.detail || error.message || 'An error occurred',
                isLoading: false
            });
        }
    }
}));
