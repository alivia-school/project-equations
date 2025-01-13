__BRYTHON__.use_VFS = true;
var scripts = {"$timestamp": 1736777827899, "core": [".py", "from browser import window\n\n\nclass Object:\n object={}\n \n def __init__(self,*args):\n  self.object=window[type(self).__name__].new(*args)\n  \n def __getattr__(self,name):\n  if name in self.object:\n   return self.object[name]\n   \n def __setattr__(self,name,value):\n  if name !='object'and name in self.object:\n   self.object[name]=value\n  else:\n   self.__dict__[name]=value\n   \n   \n   \nclass Component(Object):\n\n def __init__(self,*args,**props):\n  super().__init__(*args)\n  \n  self.element=self.object.getElement()\n  self.element.Component=self\n  \n  self.object.updatable=False\n  for prop in props:\n   if prop in self.object:\n    self.object[prop]=props[prop]\n  self.object.updatable=True\n  self.object.update()\n  \n def bind(self,*args):\n  return self.element.bind(*args)\n  \n  \n  \n  \n", ["browser"]]}
__BRYTHON__.update_VFS(scripts)
;


class Component {
    updatable = true;
    
    constructor(container, elm) {
        
        if ( container )
            container = $(container).get(0);
        
        if ( !container )
            container = $('body');
        
        elm.appendTo(container);
        
        this.e = elm
        
        // Classes
        elm.addClass('bry__component');
        let classes = [];
        for (let proto = Object.getPrototypeOf(this), cn=""; proto.constructor != Component; proto = Object.getPrototypeOf(proto)) {
            classes.unshift(proto.constructor.name)
        }
        let clss = "";
        for (const cls of classes) {
            clss += cls.toLowerCase()
            elm.addClass('bry__' + clss);
            clss += '_';
        }
        
        // Properties
        elm.find('[class^="property_"],div[class*=" property_"]').each((i,e) => {
            e = $(e);
            for (const cls of e.attr('class').split(/\s+/)) {
                if (cls.startsWith('property_')) {
                    let name = cls.slice(9);
                    this[name] = e;
                }
            }
        });
        
        // Events
        for (const name of Object.getOwnPropertyNames(Object.getPrototypeOf(this))) {
            if (name.startsWith('on') && typeof this[name] === 'function') {
                let method = this[name];
                let [ev_name, elm_name] = name.slice(2).split(/_(.*)/s);
                ev_name = ev_name.toLowerCase();
                if (elm_name)
                    this[elm_name].on(ev_name, method.bind(this));                    
                else
                    elm.on(ev_name, method.bind(this));
            }
        };
        
    }
    
    update() {
        return this.updatable;
    }
    
    getElement() {
        return this.e.get(0)
    }
    

    remove() {
        this.e.remove()
    }
    
    hide() {
        this.e.hide();
    }
    show() {
        this.e.show();
    }

    
}

