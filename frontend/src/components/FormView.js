import React, { Component } from "react";
import $ from "jquery";

import "../stylesheets/FormView.css";
import { wrapApiUrl } from "../utils/urls";

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {},
      createSuccess: null,
      ajaxErrors: null,
    };
  }

  componentDidMount() {
    $.ajax({
      url: wrapApiUrl(`/categories`), //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories });
      },
      error: (error) => {
        const errorText =
          "Unable to load categories. Please try your request again";

        alert(errorText);

        // this.setState({
        //   ajaxErrors: errorText,
        // });
      },
    });
  }

  submitQuestion = (event) => {
    this.setState({
      ajaxErrors: null,
      createSuccess: null,
    });

    event.preventDefault();
    $.ajax({
      url: wrapApiUrl("/questions"), //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState((state) => {
          return {
            createSuccess: `Question "${state.question}" successfully added!`,
            ajaxErrors: null,
          };
        });
        document.getElementById("add-question-form").reset();
      },
      error: (error) => {
        const errorText =
          "Unable to add question. Please try your request again";

        alert(errorText);

        // this.setState({
        //   ajaxErrors: errorText,
        // });
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    const { ajaxErrors, categories, createSuccess } = this.state;

    return (
      <div id="add-form">
        {ajaxErrors && (
          <h3
            style={{
              color: "red",
            }}
          >
            {ajaxErrors}
          </h3>
        )}

        {createSuccess && (
          <h3
            style={{
              color: "green",
            }}
          >
            {createSuccess}
          </h3>
        )}

        <h2>Add a New Trivia Question</h2>
        <form
          className="form-view"
          id="add-question-form"
          onSubmit={this.submitQuestion}
        >
          <label>
            Question
            <input type="text" name="question" onChange={this.handleChange} />
          </label>
          <label>
            Answer
            <input type="text" name="answer" onChange={this.handleChange} />
          </label>
          <label>
            Difficulty
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Category
            <select name="category" onChange={this.handleChange}>
              {Object.entries(categories).map(([id, category]) => {
                return (
                  <option key={id} value={id}>
                    {category}
                  </option>
                );
              })}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
