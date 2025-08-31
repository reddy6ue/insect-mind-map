/* Minimal jsMind stub for demo purposes. This is NOT a full implementation. Replace with the real jsmind.js for production. */
(function(global){
    function jsMind(options) {
        this.options = options;
    }
    jsMind.prototype.show = function(mind) {
        var container = document.getElementById(this.options.container);
        if (!container) throw new Error('jsMind: container not found');
        container.innerHTML = '<div style="padding:40px;font-size:2em;color:#888;text-align:center;">[jsMind DEMO] Mindmap would display here if real jsmind.js was loaded.<br><br>Root: ' + mind.data.topic + '</div>';
    };
    global.jsMind = jsMind;
})(window);
