var currTs = function () {
    return Math.floor(Date.now() / 1000);
};

Module.register("MMM-Smile-Gauge", {
    defaults: {
        sliderWidth: "450",  //px
        gaugeSensitivity: 0.8, // 0.1~1.0 Higher sensitivity moves gauge faster
        resetThreshold: 4, // Number of sec not seeing faces to reset gauge
        pauseThreshold: 3, // Number of sec not receiving detector signals to pause preview, set 0 to keep preview always on
        gaugeLeftText: "ChuChu's poker face", // show text when gauge reaches 0
        gaugeRightText: "Jaeger's big smile", // show text when gauge reaches 100
    },
    status: {
        lastSeenFaceTs: currTs(),
        lastDetectorTs: currTs(),
        smileValue: 50,
        preview: ''
    },
    getStyles: function() {
        return [this.file("./css/MMM-Smile-Gauge.css")];
    },
    socketNotificationReceived: function(notification, payload) {
        var self = this;
        if (notification === "UPDATE") {
            self.status.lastDetectorTs = currTs();
            const detectResult = payload;
            self.status.preview = detectResult.frame;
            if (detectResult.face_num > 0) {
                self.status.lastSeenFaceTs = currTs();
            }
            if (detectResult.smile_num > 0) {
                self.status.smileValue += detectResult.smile_num * self.config.gaugeSensitivity;
            } else {
                self.status.smileValue -= (self.config.gaugeSensitivity * 0.6);
            }
            const lastSeenFaceSec = currTs() - self.status.lastSeenFaceTs;
            if (lastSeenFaceSec > self.config.resetThreshold) {
                this.resetGauge();
            }
            self.status.smileValue = Math.min(self.status.smileValue, 100);
            self.status.smileValue = Math.max(self.status.smileValue, 0);
            self.updateDom(0);
        }
    },
    getDom: function() {
        var wrapper = document.createElement("div");
        var sliderbar = document.createElement("input");
        var gaugeLeft = document.createElement("img");
        var gaugeRight = document.createElement("img");
        var note = document.createElement("div");
        var preview = document.createElement("img");

        // HTML set up
        sliderbar.setAttribute("type", "range");
        sliderbar.setAttribute("min", "0");
        sliderbar.setAttribute("max", "100");
        sliderbar.setAttribute("style", "width:"+this.config.sliderWidth+"px");
        sliderbar.name = "sliderbar";
        gaugeLeft.src = 'MMM-Smile-Gauge/smile_left.jpg';
        gaugeRight.src = 'MMM-Smile-Gauge/smile_right.jpg';
        gaugeLeft.classList.add("circleImg");
        gaugeRight.classList.add("circleImg");
        preview.setAttribute("height", "300px");
        preview.setAttribute("width", "400px");

        // Load values from detector
        sliderbar.setAttribute("value", this.status.smileValue);
        note.innerHTML = String(Math.round(this.status.smileValue));
        preview.src = "data:image/jpeg;base64," + this.status.preview;

        // Add effect based on loaded values
        if (this.status.smileValue >= 99) {
            gaugeRight.classList.add("glow");
            note.innerHTML = this.config.gaugeRightText;
        } 
        if (this.status.smileValue <= 1) {
            gaugeLeft.classList.add("glow");
            note.innerHTML = this.config.gaugeLeftText;
        }

        wrapper.appendChild(gaugeLeft);
        wrapper.appendChild(sliderbar);
        wrapper.appendChild(gaugeRight);
        wrapper.appendChild(note);
        if (this.status.preview.length > 0) {
            wrapper.appendChild(preview);
        }
        return wrapper;
    },
    start: function() {
        var self = this;
        self.sendSocketNotification('SET_CONFIG', self.config);
        if (self.config.pauseThreshold > 0) {
            setInterval(function() {
                const lastDetectorSec = currTs() - self.status.lastDetectorTs;
                console.log(lastDetectorSec)
                if (lastDetectorSec > self.config.pauseThreshold) {
                    self.pausePreview();
                    self.updateDom(0);
                }
            }, 1200);
        }
    },
    resetGauge: function() {
        this.status.smileValue = 50;
    },
    pausePreview: function() {
        this.status.preview = '';
    }
});
