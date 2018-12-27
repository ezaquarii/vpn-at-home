const createSocket = (url) => {
    return new WebSocket(url);
};

export class DeploymentRemoteProcess {

    constructor (hostname, createSocketFunction = createSocket) {
        this.output = [];
        this.createSocket = createSocketFunction;
        this.socket = null;
        this.onStart = null;
        this.onOutput = null;
        this.onFinish = null;
        this.hostname = hostname;
    }

    connect (url) {
        if (this.socket == null) {
            this.socket = this.createSocket(url);
            this.socket.onopen = this._onOpen.bind(this);
            this.socket.onmessage = this._onMessage.bind(this);
            this.socket.onclose = this._onClose.bind(this);
            this.socket.onerror = this._onError.bind(this);
        } else {
            throw Error('Already connected');
        }
    }

    close () {
        if (this.socket) {
            this.socket.close();
        }
    }

    _onOpen () {
        const cmd = { cmd: 'start', args: { hostname: this.hostname } };
        this._sendJson(cmd);
    }

    _onMessage (message) {
        const json = JSON.parse(message.data);
        if (json.status === 'running' && json.output && this.onOutput) {
            this.onOutput(json.output);
        } else if (json.status === 'start' && this.onStart) {
            this.onStart();
        } else if (json.status === 'finished' && this.onFinish) {
            this.onFinish();
        }
    }

    _onClose () {
        // console.log('_onClose()');
    }

    _onError () {
    }

    _sendJson (obj) {
        const jsonString = JSON.stringify(obj);
        this.socket.send(jsonString);
    }

}

export class WebSocketProcess {

    constructor (args = {}, createSocketFunction = createSocket) {
        this.output = [];
        this.createSocket = createSocketFunction;
        this.socket = null;
        this.onStart = null;
        this.onOutput = null;
        this.onFinish = null;
        this.onClose = null;
        this.onError = null;
        this.args = args;
    }

    connect (url) {
        if (this.socket == null) {
            this.socket = this.createSocket(url);
            this.socket.onopen = this._onOpen.bind(this);
            this.socket.onmessage = this._onMessage.bind(this);
            this.socket.onclose = this._onClose.bind(this);
            this.socket.onerror = this._onError.bind(this);
        } else {
            throw Error('Already connected');
        }
    }

    close () {
        if (this.socket) {
            this.socket.close();
        }
    }

    _onOpen () {
        const cmd = { cmd: 'start', args: this.args };
        this._sendJson(cmd);
    }

    _onMessage (message) {
        const json = JSON.parse(message.data);
        if (json.status === 'running' && json.output && this.onOutput) {
            this.onOutput(json.output);
        } else if (json.status === 'started' && this.onStart) {
            this.onStart();
        } else if (json.status === 'finished' && this.onFinish) {
            this.onFinish();
        } else if (json.status === 'error' && this.onError) {
            this.onError();
        }
    }

    _onClose () {
        if (this.onClose) {
            this.onClose();
        }
    }

    _onError () {
        if (this.onError) {
            this.onError();
        }
    }

    _sendJson (obj) {
        const jsonString = JSON.stringify(obj);
        this.socket.send(jsonString);
    }

}
