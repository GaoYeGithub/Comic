document.getElementById('generateButton').addEventListener('click', generateComicPage);

async function generateComicPage() {
    const comicImage = document.getElementById('comicImage');
    const loadingText = document.getElementById('loading');

    comicImage.src = '';
    comicImage.style.display = 'none';
    loadingText.style.display = 'block';

    const prompt = "A single comic page, superhero fighting a villain, colorful, dynamic action scenes, with speech bubbles";

    try {
        const response = await fetch('http://127.0.0.1:5000/generate-comic', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "prompt": prompt
            })
        });        

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.generations && data.generations.length > 0 && data.generations[0].img) {
            comicImage.src = data.generations[0].img;
            comicImage.style.display = 'block';
        } else {
            throw new Error('Failed to generate comic. Please try again.');
        }

    } catch (error) {
        comicImage.alt = `Error: ${error.message}`;
        console.error('Error:', error);
    } finally {
        loadingText.style.display = 'none';
    }
}