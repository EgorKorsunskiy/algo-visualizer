import { useMutation } from "@tanstack/react-query";
import { TRecordLog } from "./types";
import { API_BASE_URL } from "@/constants";

export const useAnalyzeProgramMutation = () => useMutation({
    mutationKey: ['program'],
    mutationFn: async (program: string): Promise<TRecordLog[]> => {
        const response = await fetch(`${API_BASE_URL}/evaluator`, {
            method: "POST",
            body: JSON.stringify({ program }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        return await response.json()
    }
})