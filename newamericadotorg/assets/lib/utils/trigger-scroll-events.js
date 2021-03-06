/**
  * Loop through a list of Events and when element enters or leaves viewPort
  * assign class names and fire event callbacks, if defined.
  *
  *
  * @typedef {Object} Event
  * @property {HtmlElement[]} els - (required) an array of html elements,
  * @property {string} selector - (required) document.querySelectorAll compatable string,
  * @property {string} target - class selector, apply scroll classes to this target when element is triggered,
  * @property {string} triggerPoint - (default: 'top', options: 'top', 'middle', 'bottom') part of viewPort event is triggered,
  * @property {(number|string)} offset - (default: 0) offset for both enter and leave events. essentially shifts entire frame by this value. if defined as % (eg '50%'), offsets by % of element's outerHeight,
  * @property {(number|string)} topOffset - (default: 0) offset from triggerPoint for enter events. if defined as % (eg '50%'), offsets by % of element's outerHeight,
  * @property {(number|string)} bottomOffset - (default: 0) offset from triggerPoint for leave events. If defined as %, (eg '50%'), offsets by % of element's outerHeight,
  * @property {eventCallback} enter - event for any point after the element has passed the triggerPoint,
  * @property {eventCallback} onEnter - event for the exact moment when element hits the triggerPoint,
  * @property {eventCallback} leave - event for any point after the element (including outerHeight) is outside the triggerPoint,
  * @property {eventCallback} onLeave - event for the exact moment when element (including outerHeight) goes outside the triggerPoint
  * @property {eventCallback} onTick - when element is in view, event fires for each scroll tick.
  *
  * @callback eventCallback
  * @param {HtmlElement} el - the triggered html element
  * @param {string} direction - the direction scroll is moving ('FORWARD' or 'REVERSE')
  *
**/

const scrollEvents = (scrollPosition, prevScrollPosition, direction, events) => {
  let docHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

  const ENTER_CLASS = 'scroll-entered';
  const LEFT_CLASS = 'scroll-left';
  const IN_VIEW_CLASS = 'scroll-in-view';
  const HAS_TRIGGERED_CLASS = 'scroll-triggered';
  let oneE;
  for(let e of events){
    for(let el of e.els){
      oneE = el;
      let rect = el.getBoundingClientRect(),
      offset = getOffset(el, el.getAttribute('data-scroll-offset') || e.offset || 0 ),
      topOffset = getOffset(el, el.getAttribute('data-scroll-top-offset') || offset || e.topOffset || 0),
      bottomOffset = getOffset(el, el.getAttribute('data-scroll-bottom-offset') || offset || e.bottomOffset || 0),
      triggerPoint = el.getAttribute('data-scroll-trigger-point') || e.triggerPoint || 'top',
      triggerPointOffset = getTriggerPointOffset(triggerPoint, docHeight);

      let markedEntered = el.classList.contains(ENTER_CLASS),
      markedLeft = el.classList.contains(LEFT_CLASS),
      markedInView = el.classList.contains(IN_VIEW_CLASS),
      markedTriggered = el.classList.contains(HAS_TRIGGERED_CLASS),
      hasEntered = rect.top + topOffset + triggerPointOffset <= 0,
      hasLeft = -rect.top > el.offsetHeight + bottomOffset + triggerPointOffset,
      progress = 1-(rect.top+triggerPointOffset+el.offsetHeight+bottomOffset-0.5)/(el.offsetHeight - topOffset + bottomOffset),
      inView = hasEntered && !hasLeft;

      let targetSelector = el.getAttribute('data-scroll-target') || e.target;
      let target = targetSelector ? document.querySelector(targetSelector) : null;

      if(inView && !markedInView){
        if(e.onEnter) e.onEnter(target || el, direction);
        el.classList.remove(LEFT_CLASS);
        el.classList.add(IN_VIEW_CLASS);
        if(target){
          target.classList.remove(LEFT_CLASS);
          target.classList.add(IN_VIEW_CLASS);
        }
      }
      if(inView){
        if(e.onTick) e.onTick(target || el, direction, progress );
      }
      if(hasEntered && !markedTriggered){
        el.classList.add(HAS_TRIGGERED_CLASS);
        if(target){
          target.classList.add(HAS_TRIGGERED_CLASS);
        }
      }
      if(hasEntered && !markedEntered){
        if(e.enter) e.enter(target || el, direction);
        el.classList.remove(LEFT_CLASS);
        el.classList.add(ENTER_CLASS);
        if(target){
          target.classList.remove(LEFT_CLASS);
          target.classList.add(ENTER_CLASS);
        }
      }
      // account for scenarios where scroll speed skips over element
      if(!hasEntered && (markedInView||markedLeft||markedEntered)){
        if(e.onLeave) e.onLeave(target || el, direction);
        if(e.onTick) e.onTick(target || el, direction, rect.top > 0 ? 0 : 1);
        el.classList.remove(IN_VIEW_CLASS);
        el.classList.remove(ENTER_CLASS);
        el.classList.remove(LEFT_CLASS);
        if(target){
          target.classList.remove(IN_VIEW_CLASS);
          target.classList.remove(ENTER_CLASS);
          target.classList.remove(LEFT_CLASS);
        }
      }
      if(hasLeft && markedInView){
        if(e.onLeave) e.onLeave(target || el, direction);
        if(e.onTick) e.onTick(target || el, direction, rect.top > 0 ? 0 : 1);
        el.classList.remove(IN_VIEW_CLASS);
        el.classList.remove(LEFT_CLASS);
        if(target){
          target.classList.remove(IN_VIEW_CLASS);
          target.classList.remove(LEFT_CLASS);
        }
      }
      if(hasLeft && !markedLeft){
        if(e.leave) e.leave(target || el, direction);
        if(e.onTick) e.onTick(target || el, direction, 1);
        el.classList.add(LEFT_CLASS);
        if(target)
          target.classList.add(LEFT_CLASS);
      }
    }
  }
  // reflow
  if(oneE) void(oneE.offsetHeight);
}

export default scrollEvents;

function getOffset(el, offset) {
  if(typeof(offset)=='number') return offset;
  if(!offset) return false;
  if(offset.indexOf('%')!=-1)
    return el.offsetHeight * offset.replace('%', '')/100;
  if(offset.indexOf('vh')!=-1){
    let docHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    return docHeight * offset.replace('vh', '')/100;
  }

  return +offset;
}

function getTriggerPointOffset(triggerPoint, docHeight){
  switch(triggerPoint){
    case 'top':
      return 0;
    case 'bottom':
      return -docHeight;
    case 'middle':
      return -docHeight/2;
    default:
      return 0;
  }
}
