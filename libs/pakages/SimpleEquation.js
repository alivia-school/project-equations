__BRYTHON__.use_VFS = true;
var scripts = {"$timestamp": 1732469726143, "Equation": [".py", "from browser import window\nfrom core import Object\n\nclass Equation(Object):\n def __init__(self,value=\"\"):\n  super().__init__(value)\n  \nclass EquationComponent(Object):\n def __init__(self,value,factor_value=\"\"):\n  super().__init__(value,factor_value)\n  \nEquationComponentType=window.EquationComponentType\n\n\n\n", ["browser", "core"]], "SimpleEquationComponent": [".py", "from browser import window\nfrom core import Component\n\nclass SimpleEquation(Component):\n\n def __init__(self,container=\"\",**props):\n  super().__init__(container,**props)\n", ["browser", "core"]]}
__BRYTHON__.update_VFS(scripts)
;
(function(){const __$tmp = document.createElement("style");__$tmp.textContent = `
.bry__simpleequation {
    position: relative;
    border: 1px solid var(--component-border-color);
    border-radius: var(--component-border-radius);
    font-size: 120%;
    margin: 20px 0 calc(50px * var(--scale, 1)) 0;  

    --placeholder: "Input an equation";
    --notice-error: "The equation contains error(s)";    
}

.bry__simpleequation .property_text {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    background-color: white;
    border-radius: inherit;
    padding: var(--component-padding);
    cursor: text;
}
.bry__simpleequation:not(.read-only) .property_text {
    user-select: none;
}

.bry__simpleequation .property_text:empty::before {
   content: var(--placeholder);
   color: var(--component-placeholder-color);
   font-size: 90%;
}    

.bry__simpleequation.error .property_input {
    outline: var(--component-error-color) solid;
}      
.bry__simpleequation.error .property_text::before {
   content: var(--notice-error);
   color: var(--component-error-color);
   font-size: 70%;
   position: absolute;
   top: calc(100% + 1px);
   left: 0;
   right: 0;
}  

.bry__simpleequation .property_input {
    width: 100%;
    text-align: inherit;
    font: inherit;
    border: none;
    border-radius: inherit;
    padding: var(--component-padding) 0;
}

.bry__simpleequation.read-only  {
    border: none;
}
.bry__simpleequation.read-only .property_input {
    visibility: hidden;
    height: 0;
}
.bry__simpleequation.read-only .property_text {
    padding: 0;
}

.bry__simpleequation .property_input:focus-visible {
    outline: var(--component-outline-focus-color) solid;
}`;document.head.appendChild(__$tmp);})();
EquationComponentType = {
    Empty: 0,    
    Equal: 1,    
    Parentheses: 2,
    Number: 3,
    Operation: 4,
    Unknown: 5
}

class EquationComponent  {
    
    constructor(value, factor_value='') {
        
        if (value instanceof EquationComponent) {
            // Clone from value
            this.value = value.value;
            this.factor_value = value.factor_value;
            this.type = value.type;
            this.as_factor = value.as_factor;
            this.element = value.element.clone();
        } else {
            this.value = value
            this.factor_value = factor_value;
            this.as_factor = false;
            
            if ( value === '' )
                this.type = EquationComponentType.Empty;            
            else if ( value === '=' )
                this.type = EquationComponentType.Equal;
            else if ( ['(', ')'].includes(value) )
                this.type = EquationComponentType.Parentheses;
            else if ( ['+', '-'].includes(value) )
                this.type = EquationComponentType.Operation;
            else if ( typeof value === 'number' )
                this.type = EquationComponentType.Number;
            else
                this.type = EquationComponentType.Unknown;
                                
            this.element =  $('<span>' + (factor_value==1?'':factor_value) + value + '</span>');
            
            if (this.type == EquationComponentType.Unknown && !factor_value)
                this.factor_value = 1
        }
        
    } 
    
    set color(val) {
        this.element.css('color', val);
    }
    get color() {
        return this.element.css('color');
    } 
    
}


class Equation  {
    
    #value = ""
    
    error = false
    components = [];
    unknown = '';
    
    constructor(value="") {
        if (value) {
            this.value = value
        }
    }    
    
    copy(from) {
        this.#value = from.value;
        this.error = from.error;
        this.unknown = from.unknown;
        // copy components
        this.components = [];
        for (const component of from.components) {
            this.components.push(new EquationComponent(component))
        }
        this.update();        
    }
    
    equal(equation) {
        return (this.value.replace(/ /g,'') === equation.value.replace(/ /g,''));  
    }
    isSame(equation) {
        return (this.value.replace(/ /g,'') === equation.replace(/ /g,''))
    }
    
    left() {
        var r = [];
        
        for (const component of this.components) {
            if (component.type == EquationComponentType.Equal) {
                break;
            }
            r.push(component);
        }     
        return r;
    }
 
    rigth() {
        var r = [];
        var b = false;
        
        for (const component of this.components) {
            if (component.type == EquationComponentType.Equal) {
                b = true;
                continue;
            }
            if (b) {
                r.push(component);
            }
        }     
        return r;
    }
    
    update() {}
    
    #parse() {
        var error = false;
        var val = this.value.replace(/ /g,'');
        var components = []
        
        if (val != "") {
        
            let collected = {
                    cur_number: '',
                    cur_x: undefined,
                    eqs: 0,
                    Parenthesess: 0,
                }
                
            function checkNumber() {
                if (collected.cur_number !== '') {
                    components.push(new EquationComponent(parseInt(collected.cur_number)));
                    collected.cur_number = '';                     
                }                    
            }                
            
            for (let i = 0; i < val.length && !error; i++) {
                let c = val[i];
                
                if (c >= '0' && c <= '9') {
                    collected.cur_number += c; 
                    continue;
                }
                checkNumber()

                if ((c > 'a' && c < 'z')) {
                    if ( !collected.cur_x ) {
                        collected.cur_x = c; 
                    } else if ( collected.cur_x != c) {
                        error = true 
                        continue
                    }
                    if (components.length > 0) {
                        let lastComponent = components.slice(-1)[0];
                        if (lastComponent.type == EquationComponentType.Number) {
                            if (lastComponent.value == 0) {
                                error = true 
                                continue
                            }
                            components.pop();
                            components.push(new EquationComponent(c, lastComponent.value));
                            continue;
                        } 
                    }
                    components.push(new EquationComponent(c));
                    continue;
                }
                
                switch (c) {
                                        
                    case '=':
                        collected.eqs++;
                        if (collected.Parenthesess!=0)
                            error = true
                        break;
                        
                    case '(':
                        collected.Parenthesess++;
                        break
                        
                    case ')':
                        collected.Parenthesess--;
                        break;
                        
                    case '+':
                    case '-':
                        break;                    
                        
                    default:
                        error = true
                }
                
                if (collected.Parenthesess>1)
                    error = true 
                    
                if (!error)
                    components.push(new EquationComponent(c));
                else
                    break

            }
            checkNumber()
            
            if (collected.eqs!=1 || collected.Parenthesess!=0 || !collected.cur_x)
                error = true 
            
            this.components = components.slice(0);
            this.unknown = collected.cur_x
            
            components.unshift(new EquationComponent(''));        
            components.push(new EquationComponent(''));  
            for (let i = 1; i < components.length-1 && !error; i++) {
                let value = components[i].value;
                let type = components[i].type;
                
                switch (type) {
                    case EquationComponentType.Operation:
                        error = !(   [...(value=='-' ? [EquationComponentType.Empty, EquationComponentType.Equal] : []), EquationComponentType.Number, EquationComponentType.Parentheses, EquationComponentType.Unknown].includes(components[i-1].type) 
                                  && [EquationComponentType.Number, EquationComponentType.Parentheses, EquationComponentType.Unknown].includes(components[i+1].type))
                        break;
                    case EquationComponentType.Unknown:
                        error = ( [EquationComponentType.Unknown, EquationComponentType.Number].includes(components[i+1].type))
                        break;
                    case EquationComponentType.Parentheses:
                        error = ( [...(value==')' ? [EquationComponentType.Number, EquationComponentType.Unknown] : []), EquationComponentType.Parentheses].includes(components[i+1].type))
                        break;
                    case EquationComponentType.Equal:
                        error = ( [EquationComponentType.Empty].includes(components[i+1].type) )
                        break;
                }
                            
                if (type == EquationComponentType.Equal || (i != 1 && components[i-1].type != EquationComponentType.Equal && type == EquationComponentType.Operation)) {
                    components[i].element.text(' ' + components[i].element.text() + ' ')
                }

            }
        }
        
        if (!error) {
            //Check parentheses factor
            let inBlock = false;
            let curFactor = new EquationComponent('');
            for (const component of this.components) {
                if (component.value == '(') {
                    inBlock = true;
                    if (curFactor.type != EquationComponentType.Operation)
                        curFactor.as_factor = true;
                } else if (component.value == ')') {
                    inBlock = false;            
                    curFactor = new EquationComponent('');
                } else if (inBlock) {
                    if (    curFactor.value == 0
                        || (curFactor.type == EquationComponentType.Unknown && component.value == curFactor.value)) {
                        error = true;
                        break
                    }
                } else {
                    curFactor = component
                }
            }
        }
        
           
        this.error = error;
        
        if (error || val === "") {
            this.components = [];
            this.unknown = '';
        }
                
    }
    
    fillTo(container) {
        container.empty();
        for (const component of this.components)
            component.element.appendTo(container);
    }
    

    /* value property */
    set value(val) {
        this.#value = val.toLowerCase();
        this.#parse();
        this.update();
    }
    get value() {
        return this.#value;
    }   
        
}

window.Equation = Equation
window.EquationComponent = EquationComponent;
;

class SimpleEquation extends Component {
       
    #equation
    #readOnly = false

    constructor(container) {        
        var e = $(`
            <div>
                <div class="property_text"></div>
                <input class="property_input" type="text" name="input">    
            </div>
        `);
        super(container, e);  

        this.#equation = new Equation() 
        this.#equation.update = () => {
            if ( !this.#equation.error ) {
                this.#equation.fillTo(this.text);
                this.input.val(this.text.text()); 
            } else {
                this.input.val(this.#equation.value)
                this.text.text(this.#equation.value);
            }                
                
            this.e.toggleClass("error", this.#equation.error);
        }
        
    }    
    
    onClick(ev) {
        this.input.focus();
    }

    onBlur_input(ev) {
        this.text.show();
        let val = this.input.val().trim();
        if ( !this.#equation.isSame(val) ) {
            this.#equation.value = val;
        }
        this.input.val(this.text.text());        
    }
    onFocus_input(ev) {
        if ( this.readOnly ) 
            return
        this.text.hide();
    }
    
    onKeypress(ev) {
         if(ev.which == 13) {
            this.input.blur();
        }
    }
    
    before(e) {
        $(e).before(this.e);
    }
    after(e) {
        $(e).after(this.e);
    }       
       
    /* readOnly property */
    set readOnly(val) {
        this.#readOnly = val;
        this.e.toggleClass("read-only", val)
    }
    get readOnly() {
        return this.#readOnly;
    } 
    
    /* equation property */
    set equation(val) {
        this.#equation.copy(val);
    }
    get equation() {
        return this.#equation;
    } 
    
    /* placeholder property */
    set placeholder(val) {
        this.e.css("--placeholder", val ? '"'+val+'"' : '')
    }
    get placeholder() {
        return this.e.css("--placeholder");
    } 
    
}

window.SimpleEquation = SimpleEquation