import { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { setTemplateUrl, fetchTemplate } from '../actions';
import { BASEURL } from '../constants';

class Template extends Component {

  componentWillMount() {
    this.props.getTemplate(this.props.baseUrl+this.props.endpoint);
  }

  static propTypes = {
    name: PropTypes.string.isRequired,
    endpoint: PropTypes.string.isRequired,
    baseUrl: PropTypes.string,
    renderedTemplate: PropTypes.string
  }

  static defaultProps = {
    baseUrl: BASEURL
  }

  render() {
    return (
      <div dangerouslySetInnerHTML={{__html:this.props.renderedTemplate.html}}></div>
    )
  }
}

const mapStateToProps = (state,props) => ({
  renderedTemplate: state[props.name] ? state[props.name].rendered : ''
});

const mapDispatchToProps = dispatch => ({
  getTemplate: function(url){
    dispatch(setTemplateUrl(this.name, url));
    dispatch(fetchTemplate(this.name));
  }
});

export default connect(
  mapStateToProps, mapDispatchToProps
)(Template);
