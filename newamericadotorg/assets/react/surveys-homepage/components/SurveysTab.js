import React from 'react';
import CheckboxGroup from './CheckboxGroup';
import TeaserListing from './TeaserListing';
import CtaCard from './CtaCard';
import Search from './Search';
import './SurveysTab.scss';

class SurveysTab extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filtersOpen: false,
      search: {
        q: '',
      },
      tags: this.props.data.survey_home_page.surveys.reduce(
        (acc, cur) => {
          const tags = cur['tags'];
          tags.forEach((tag, i) => {
            acc[tag.title] = false;
          });

          return acc;
        },
        {}
      ),
      demos: this.props.data.survey_home_page.surveys.reduce(
        (acc, cur) => {
          const demos = cur['demos_key'];

          demos.forEach((demo, i) => {
            acc[demo.title] = false;
          });

          return acc;
        },
        {}
      ),
      orgs: this.props.data.survey_home_page.surveys.reduce(
        (acc, cur) => {
          const orgs = cur['org'];

          orgs.forEach((org, i) => {
            acc[org.title] = false;
          });

          return acc;
        },
        {}
      ),
      dateRange: {
        dateOne: false,
        dateTwo: false,
        dateThree: false,
        dateFour: false,
        dateFive: false,
      },
      sizeRange: {
        sizeOne: false,
        sizeTwo: false,
        sizeThree: false,
        sizeFour: false,
      },
      dataType: {
        Qual: false,
        Quant: false,
        'Mixed Methods': false,
      },
      national: {
        represented: false,
        notRepresented: false,
      },
    };
  }

  onFilterChange = (name, filter) => {
    this.setState({ [name]: filter });
  };

  handleSearchInput = (q) => {
    this.setState({ search: { q: q } });
  };

  toggleMobileFilters = () => {
    this.setState({
      filtersOpen: !this.state.filtersOpen,
    });
  };

  render() {
    const { tags, demos, orgs, filtersOpen } = this.state;
    let newState = { ...this.state };

    const submission = JSON.parse(this.props.data.survey_home_page.submissions)[0].value ?
      JSON.parse(this.props.data.survey_home_page.submissions)[0].value :
      false
    const subscribe = JSON.parse(this.props.data.survey_home_page.subscribe)[0].value ?
      JSON.parse(this.props.data.survey_home_page.subscribe)[0].value :
      false

    Object.keys(newState).forEach((key, index) => {
      const { isOpen, ...rest } = newState[key];
      newState[key] = rest;
    });

    return (
      <div className="surveys-tab">
        <Search
          title="Search for Survey Reports"
          handleSearchInput={this.handleSearchInput}
        />
        <div className="surveys-tab__inner">
          <div
            className={`surveys-tab__open-mobile-filter col-12 margin-top-35 margin-bottom-25`}
          >
            <a
              className={`button--text with-caret--${
                filtersOpen ? 'up' : 'down'
              }`}
              onClick={this.toggleMobileFilters}
            >
              Filters
            </a>
          </div>
          <div
            className={`surveys-tab__sidebar ${
              filtersOpen ? 'is-open' : ''
            }`}
          >
            <CheckboxGroup
              title="Topic"
              options={Object.keys(tags)
                .map((tag) => ({
                  id: tag,
                  checked: false,
                  label: tag.charAt(0).toUpperCase() + tag.slice(1),
                }))
                .sort((a, b) => {
                  return a.label.localeCompare(b.label);
                })}
              onChange={(filterState) =>
                this.onFilterChange('tags', filterState)
              }
            />

            <CheckboxGroup
              title="Demographic"
              options={Object.keys(demos)
                .map((demo) => ({
                  id: demo,
                  checked: false,
                  label: demo.charAt(0).toUpperCase() + demo.slice(1),
                }))
                .sort((a, b) => {
                  return a.label.localeCompare(b.label);
                })}
              onChange={(filterState) =>
                this.onFilterChange('demos', filterState)
              }
            />
            <CheckboxGroup
              title="Publication Date"
              options={[
                {
                  checked: false,
                  label: 'Last 3 months',
                  id: 'dateOne',
                },
                {
                  checked: false,
                  label: 'Last 6 months',
                  id: 'dateTwo',
                },
                {
                  checked: false,
                  label: 'Within 1 year',
                  id: 'dateThree',
                },
                {
                  checked: false,
                  label: 'Within 2 years',
                  id: 'dateFour',
                },
                {
                  checked: false,
                  label: '2+ years ago',
                  id: 'dateFive',
                },
              ]}
              onChange={(filterState) =>
                this.onFilterChange('dateRange', filterState)
              }
            />
            <CheckboxGroup
              title="Sample Size"
              options={[
                { checked: false, label: '< 1,000', id: 'sizeOne' },
                {
                  checked: false,
                  label: '1,000 - 5,000',
                  id: 'sizeTwo',
                },
                {
                  checked: false,
                  label: '5,000 - 10,000',
                  id: 'sizeThree',
                },
                { checked: false, label: '> 10,000', id: 'sizeFour' },
              ]}
              onChange={(filterState) =>
                this.onFilterChange('sizeRange', filterState)
              }
            />
            <CheckboxGroup
              title="Organization"
              options={Object.keys(orgs)
                .map((org) => ({
                  id: org,
                  checked: false,
                  label: org.charAt(0).toUpperCase() + org.slice(1),
                }))
                .sort((a, b) => {
                  return a.label.localeCompare(b.label);
                })}
              onChange={(filterState) =>
                this.onFilterChange('orgs', filterState)
              }
            />

            <CheckboxGroup
              title="Type of Data"
              options={[
                { checked: false, label: 'Qualitative', id: 'qual' },
                {
                  checked: false,
                  label: 'Quantitative',
                  id: 'quant',
                },
                {
                  checked: false,
                  label: 'Mixed Methods',
                  id: 'mixed',
                },
              ]}
              onChange={(filterState) =>
                this.onFilterChange('dataType', filterState)
              }
            />

            <CheckboxGroup
              title="Sample Representaion"
              options={[
                {
                  checked: false,
                  label: 'Nationally Represented',
                  id: 'represented',
                },
                {
                  checked: false,
                  label: 'Not Nationally Represented',
                  id: 'notRepresented',
                },
              ]}
              onChange={(filterState) =>
                this.onFilterChange('national', filterState)
              }
            />
            <div className="margin-top-25 d-xs-none">
              {submission && (
                <CtaCard
                      type="email"
                      title={submission.title}
                      description={submission.description}
                      url={submission.link_url}
                      linkText={submission.link_text}
                    />
              )}
            </div>
          </div>
          <div className="surveys-tab__results">
            <TeaserListing
              data={this.props.data.survey_home_page.surveys}
              checkedValues={newState}
              searchTerm={newState.search.q}
            />
            <div className="margin-top-60">
              <div className="d-sm-none margin-bottom-10">
                {submission && (
                    <CtaCard
                    type="email"
                    title={submission.title}
                    description={submission.description}
                    url={submission.link_url}
                    linkText={submission.link_text}
                  />
                )}
              </div>
              {subscribe && (
                <CtaCard
                  type="link"
                  title={subscribe.title}
                  description={subscribe.description}
                  url={subscribe.link_url}
                  linkText={subscribe.link_text}
                />
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default SurveysTab;
