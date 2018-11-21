const createSocket = (url) => {
    return new WebSocket(url);
};

export class RemoteProcess {

    constructor (createSocketFunction = createSocket) {
        this.output = [];
        this.createSocket = createSocketFunction;
        this.socket = null;
        this.onStart = null;
        this.onOutput = null;
        this.onFinish = null;
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
        this._sendJson({ cmd: 'start' });
    }

    _onMessage (message) {
        const json = JSON.parse(message.data);
        if (json.status === 'running' && json.output && this.onOutput) {
            this.onOutput(json.output);
        } else if (json.status === 'start' && this.onStart) {
            this.onStart();
        } else if (json.status === 'finish' && this.onFinish) {
            this.onFinish();
        } else {
            console.log('_onMessage(): unknown message', json);
        }
    }

    _onClose () {
        // console.log('_onClose()');
    }

    _onError () {
        // console.log('_onError()');
    }

    _sendJson (obj) {
        const jsonString = JSON.stringify(obj);
        this.socket.send(jsonString);
    }

}
