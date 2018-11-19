const net = require('net');
const fs = require('fs');
const path = require('path');
const NodeHelper = require('node_helper');
const spawn = require('child_process').spawn;

const socketPath = '/tmp/node-python-socket';
const msgSeperator = "\r";

module.exports = NodeHelper.create({
    config: {
        autoStartDetector: true
    },
    start: function() {
        var self = this;
        fs.unlink(socketPath,
            () => net.createServer(function(socket) {
                // Quick solution for splitted message from client (max size 1024bytes)
                var dataStr = '';
                socket.on('data', (data) => {
                    dataStr += data.toString();

                    var msgSeperatorIndex = dataStr.indexOf(msgSeperator);
                    var foundMsg = msgSeperatorIndex != -1;

                    if (foundMsg) {
                        var msg = dataStr.slice(0, msgSeperatorIndex);
                        const detectResult = JSON.parse(msg);
                        self.sendSocketNotification('UPDATE', detectResult);
                        dataStr = dataStr.slice(msgSeperatorIndex+1);
                    } 
                });
            }).listen(socketPath, function(err) {
                if (self.config.autoStartDetector) {
                    if (err) throw err;
                    const detectorSocketPath = path.join(self.path, 'detector', 'detector_socket.py');
                    const detectorClient = spawn('python', [detectorSocketPath]);
                    detectorClient.stdout.on('data', (data) => {
                        console.log('stdout: ', data.toString());
                    });
                    detectorClient.stderr.on('data', (data) => {
                        console.log('stderr: ', data.toString());
                    });
                    detectorClient.on('error', (err) => {
                        console.log('Failed to start subprocess.', err.toString());
                    });
                    detectorClient.on('close', (code) => {
                        console.log('subprocess exited with code ', code.toString());
                    });
                }
            })
        );

    },
    socketNotificationReceived: function(notification, payload) {
        if (notification === "SET_CONFIG") {
            this.config = payload;
        }
    }
});
