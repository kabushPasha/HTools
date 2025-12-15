export function playSound(sound,vol=0.01) {
    const snd = new Audio(sound);
    snd.volume = vol;
    snd.play();
}