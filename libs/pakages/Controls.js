__BRYTHON__.use_VFS = true;
var scripts = {"$timestamp": 1731012885523, "Controls.Button": [".py", "from Controls import Control\n\nclass Button(Control):\n\n def __init__(self,container=\"\",**props):\n  super().__init__(container,**props)\n", ["Controls"]], "Controls": [".py", "from core import Component\n\nclass Control(Component):\n\n def __init__(self,container=\"\",**props):\n  super().__init__(container,**props)\n", ["core"], 1]}
__BRYTHON__.update_VFS(scripts)
;
(function(){const __$tmp = document.createElement("style");__$tmp.textContent = `.bry__control {
    font-size: 100%;
    padding: var(--component-padding);
    border: 1px solid var(--component-border-color);
    border-radius: var(--component-border-radius);
}

.bry__control_button {
    min-width: 200px;
    cursor: pointer;
}`;document.head.appendChild(__$tmp);})();
class Control extends Component {
    
    constructor(container, e) {                      
        super(container, e);             
    }
    
    /* text  property */
    set text(val) {
        this.e.text(val);
    }
    get speed() {
        this.e.text();
    }
        
}
;

class Button extends Control {
    
    constructor(container) {   
        var e = $('<button></button>');
        
        super(container, e);
    }

}

window.Button = Button