export default class ColorGenerator {
    static hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : { r: 0, g: 0, b: 0 };
    }

    static colorDistance(hexColorF, hexColorS) {
        const rgb1 = this.hexToRgb(hexColorF);
        const rgb2 = this.hexToRgb(hexColorS);
        return Math.sqrt(
            Math.pow(rgb1.r - rgb2.r, 2) +
            Math.pow(rgb1.g - rgb2.g, 2) +
            Math.pow(rgb1.b - rgb2.b, 2)
        );
    }

    static generateRandomHex() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    static generateDistinctColor(existingColors = {}) {
        const existing = Object.values(existingColors).filter(c => typeof c === 'string' && c.startsWith('#'));

        if (existing.length === 0) {
            let color = this.generateRandomHex();
            while (color === '#000000' || color === '#FFFFFF') {
                color = this.generateRandomHex();
            }
            return color;
        }

        let bestColor = '#FF00FF';
        let maxMinDistance = -1;
        const attempts = 300;

        for (let i = 0; i < attempts; i++) {
            let candidate = this.generateRandomHex();

            while (candidate === '#000000' || candidate === '#FFFFFF') {
                candidate = this.generateRandomHex();
            }

            let minDistance = Infinity;
            for (const exColor of existing) {
                const dist = this.colorDistance(candidate, exColor);
                if (dist < minDistance) minDistance = dist;
            }

            if (minDistance > maxMinDistance) {
                maxMinDistance = minDistance;
                bestColor = candidate;
            }
        }

        return bestColor;
    }
}
