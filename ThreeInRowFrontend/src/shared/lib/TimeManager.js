export class TimeManager {
    static gameLooseTime = 1000 * 3600 * 2;

    static msToTotalHoursTime(duration) {
        let seconds = Math.floor((duration / 1000) % 60);
        let minutes = Math.floor((duration / (1000 * 60)) % 60);
        let hours = Math.floor(duration / (1000 * 60 * 60));

        hours = hours.toString().padStart(2, '0');
        minutes = minutes.toString().padStart(2, '0');
        seconds = seconds.toString().padStart(2, '0');

        return `${hours}:${minutes}:${seconds}`;
    }

    static ssToTotalHoursTime(duration) {
        let seconds = Math.floor(duration  % 60);
        let minutes = Math.floor(duration / 60 % 60);
        let hours = Math.floor(duration / (60 * 60));

        hours = hours.toString().padStart(2, '0');
        minutes = minutes.toString().padStart(2, '0');
        seconds = seconds.toString().padStart(2, '0');

        return `${hours}:${minutes}:${seconds}`;
    }
}