__BRYTHON__.use_VFS = true;
var scripts = {"$timestamp": 1736692452375, "Controls.Button": [".py", "from Controls import Control\n\nclass Button(Control):\n\n def __init__(self,container=\"\",**props):\n  super().__init__(container,**props)\n", ["Controls"]], "Controls.Label": [".py", "from Controls import Control\n\nclass Label(Control):\n\n def __init__(self,container=\"\",**props):\n  super().__init__(container,**props)\n", ["Controls"]], "Controls": [".py", "from core import Component\n\nclass Control(Component):\n\n def __init__(self,container=\"\",**props):\n  super().__init__(container,**props)\n", ["core"], 1]}
__BRYTHON__.update_VFS(scripts)
;
(function(){const __$tmp = document.createElement("style");__$tmp.textContent = `.bry__control {
    font-size: 100%;
    padding: var(--component-padding);
    border: 1px solid var(--component-border-color);
    border-radius: var(--component-border-radius);
}

.bry__control_button {
    cursor: pointer;
}

.bry__control_label {
    border: none;
    text-align: left;    
}`;document.head.appendChild(__$tmp);})();
class Control extends Component {
    
    constructor(container, e) {                      
        super(container, e);             
    }
    
    hide() {
        this.e.hide();
    }
    show() {
        this.e.show();
    }
    
    /* text  property */
    set text(val) {
        this.e.text(val);
    }
    get text() {
        return this.e.text();
    }
        
}
;

class Button extends Control {
    
    constructor(container) {   
        var e = $('<button></button>');
        
        super(container, e);
    }

}

window.Button = Button;

class Label extends Control {
    
    constructor(container) {   
        var e = $('<pre></pre>');
        
        super(container, e);
    }

}

window.Label = Label