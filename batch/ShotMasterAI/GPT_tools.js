const GPT = {
    async txt2txt(input) {        
        try {
        const res = await fetch("https://api.openai.com/v1/chat/completions", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${window.userdata.GPT_API_KEY}`
            },
            body: JSON.stringify({
            model: "gpt-3.5-turbo", // or "gpt-4" if your key has access
            messages: [
                { role: "system", content: "You are a helpful assistant." },
                { role: "user", content: input }
            ]
            })
        });

        const data = await res.json();
        console.log(data);
        } catch (err) {
        output.textContent = "Error: " + err.message;
        }        
    }

}

const OpenRouter = {
    async txt2txt(input) {

        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${window.userdata.openrouter_API_KEY}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "model": "openai/gpt-oss-20b:free",
                "messages": [
                {
                    "role": "user",
                    "content": input
                }
                ],
                "reasoning": {"enabled": true}
                })
            });

        const result = await response.json();
        message = result.choices[0].message;
        console.log(message);
        console.log(message.content);
        return message.content;
    }

}

