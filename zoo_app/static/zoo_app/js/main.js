// main.js - gate open + confetti
(function(){
    const hero = document.getElementById('heroWrap');
    const openBtn = document.getElementById('openGateBtn');
    const confettiCanvas = document.getElementById('confettiCanvas');

    // Resize canvas to cover hero
    function fitCanvas() {
        if (!confettiCanvas) return;
        confettiCanvas.width = hero.clientWidth;
        confettiCanvas.height = hero.clientHeight;
        confettiCanvas.style.width = hero.clientWidth + 'px';
        confettiCanvas.style.height = hero.clientHeight + 'px';
    }
    window.addEventListener('resize', fitCanvas);
    window.addEventListener('load', fitCanvas);
    setTimeout(fitCanvas, 100);

    // tiny floating title effect
    const title = document.querySelector('.hero-title');
    if (title) {
        let t=0;
        (function floatTitle(){
        t+=0.01;
        title.style.transform = `translateY(${Math.sin(t)*3}px)`;
        requestAnimationFrame(floatTitle);
        })();
    }

    // Confetti engine
    function startConfetti(duration = 2000) {
        if (!confettiCanvas) return;
        const ctx = confettiCanvas.getContext('2d');
        const W = confettiCanvas.width;
        const H = confettiCanvas.height;
        const pieces = [];
        const colors = ['#ffbe0b','#fb5607','#ff006e','#8338ec','#3a86ff','#13c08b'];

        for (let i=0;i<120;i++){
        pieces.push({
            x: Math.random() * W,
            y: Math.random() * -H,
            r: 6 + Math.random()*10,
            d: (Math.random()*50)+10,
            color: colors[Math.floor(Math.random()*colors.length)],
            tilt: Math.random()*10 - 10,
            tiltAngleIncrement: (Math.random()*0.07)+0.05,
            tiltAngle: 0
        });
        }

        let start = performance.now();
        function update(now){
        const elapsed = now - start;
        ctx.clearRect(0,0,W,H);
        for (let i=0;i<pieces.length;i++){
            const p = pieces[i];
            p.tiltAngle += p.tiltAngleIncrement;
            p.y += Math.cos(p.d) + 3 + p.r/10;
            p.x += Math.sin(p.d);
            p.tilt = Math.sin(p.tiltAngle) * 12;
            ctx.beginPath();
            ctx.fillStyle = p.color;
            // draw small rotated rectangle as confetti
            ctx.save();
            ctx.translate(p.x + p.tilt, p.y);
            ctx.rotate(p.tilt * 0.02);
            ctx.fillRect(-p.r/2, -p.r/2, p.r*1.6, p.r);
            ctx.restore();
        }
        if (elapsed < duration) {
            requestAnimationFrame(update);
        } else {
            // fade out
            ctx.clearRect(0,0,W,H);
        }
        }
        requestAnimationFrame(update);
    }

    // Button click opens gate & triggers confetti & redirect
    if (openBtn && hero) {
        openBtn.addEventListener('click', function(){
        // add class -> CSS rotates gates open and sharpens bg
        hero.classList.add('open');

        // play confetti shortly after opening
        setTimeout(()=> startConfetti(1700), 220);

        // change button text
        openBtn.disabled = true;
        openBtn.textContent = "Opening...";

        // redirect after animation done (~900ms)
        setTimeout(()=> {
            window.location.href = "/swagger/";
        }, 1000);
        });
    }
})();
// /* =============================
//    ANIMALS ON GATE (cute idle)
//    ============================= */
(function(){
    const canvas = document.getElementById('gateAnimalsCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function fitCanvas(){
        canvas.width = window.innerWidth;
        canvas.height = 180;
    }
    fitCanvas();
    window.addEventListener('resize', fitCanvas);

    // Class mô phỏng con vật
    class GateAnimal {
        constructor(x, color){
        this.x = x;
        this.y = 100;
        this.color = color;
        this.scale = 0.9 + Math.random()*0.3;
        this.phase = Math.random()*Math.PI*2;
        this.blinkTimer = Math.random()*3000 + 1000;
        this.blink = false;
        this.jumping = false;
        this.jumpProgress = 0;
        }

        draw(t){
        ctx.save();
        ctx.translate(this.x, this.y);
        const bob = Math.sin(t*0.002 + this.phase) * 4;
        ctx.translate(0, -bob);

        // body
        ctx.beginPath();
        ctx.fillStyle = this.color;
        ctx.ellipse(0, 0, 18*this.scale, 14*this.scale, 0, 0, Math.PI*2);
        ctx.fill();

        // head
        ctx.beginPath();
        ctx.fillStyle = shade(this.color, -10);
        ctx.arc(0, -16*this.scale, 10*this.scale, 0, Math.PI*2);
        ctx.fill();

        // eyes
        ctx.fillStyle = '#111';
        if (!this.blink) {
            ctx.beginPath(); ctx.arc(-4*this.scale, -17*this.scale, 2*this.scale, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(4*this.scale, -17*this.scale, 2*this.scale, 0, Math.PI*2); ctx.fill();
        } else {
            ctx.fillRect(-5*this.scale, -17*this.scale, 3*this.scale, 1*this.scale);
            ctx.fillRect(2*this.scale, -17*this.scale, 3*this.scale, 1*this.scale);
        }

        // tail wag
        ctx.save();
        const wag = Math.sin(t*0.01 + this.phase) * 10;
        ctx.rotate((wag*Math.PI)/180);
        ctx.beginPath();
        ctx.strokeStyle = shade(this.color, -30);
        ctx.lineWidth = 2;
        ctx.moveTo(-14*this.scale, 2*this.scale);
        ctx.lineTo(-24*this.scale, 8*this.scale);
        ctx.stroke();
        ctx.restore();

        ctx.restore();
        }

        update(dt){
        this.blinkTimer -= dt;
        if (this.blinkTimer < 0){
            this.blink = !this.blink;
            this.blinkTimer = this.blink ? 100 : Math.random()*3000+1000;
        }
        // Jump animation
        if (this.jumping){
            this.jumpProgress += dt*0.004;
            const jumpY = -Math.sin(Math.min(this.jumpProgress, Math.PI))*60;
            this.y = 100 + jumpY;
            if (this.jumpProgress > Math.PI*1.2) this.jumping = false;
        }
        }
    }

    // Helper để làm màu đậm hơn tí
    function shade(color, percent){
        const num = parseInt(color.replace("#",""),16);
        const amt = Math.round(2.55 * percent);
        const R = (num >> 16) + amt;
        const G = (num >> 8 & 0x00FF) + amt;
        const B = (num & 0x0000FF) + amt;
        return "#" + (
        0x1000000 + 
        (R<255?(R<1?0:R):255)*0x10000 +
        (G<255?(G<1?0:G):255)*0x100 +
        (B<255?(B<1?0:B):255)
        ).toString(16).slice(1);
    }

    // Tạo vài con vật
    const colors = ['#ffad60','#ff6666','#7cc6fe','#77dd77','#dba9ff'];
    const animals = [new GateAnimal(300,colors[0]),
                    new GateAnimal(420,colors[1]),
                    new GateAnimal(540,colors[2]),
                    new GateAnimal(660,colors[3])];

    let last = performance.now();
    function loop(now){
        const dt = now - last;
        last = now;
        ctx.clearRect(0,0,canvas.width,canvas.height);
        for (const a of animals){
        a.update(dt);
        a.draw(now);
        }
        requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);

    // Khi nhấn nút mở cổng => cho thú nhảy xuống
    const openBtn = document.getElementById('openGateBtn');
    openBtn.addEventListener('click', ()=>{
        animals.forEach((a,i)=>{
        setTimeout(()=>a.jumping=true, i*180);
        });
    });
})();
