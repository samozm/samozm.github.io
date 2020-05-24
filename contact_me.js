//import React from "react";
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var PersonalContact = function (_React$Component) {
    _inherits(PersonalContact, _React$Component);

    function PersonalContact(props) {
        _classCallCheck(this, PersonalContact);

        var _this = _possibleConstructorReturn(this, (PersonalContact.__proto__ || Object.getPrototypeOf(PersonalContact)).call(this, props));

        _this.submitForm = _this.submitForm.bind(_this);
        _this.state = {
            status: ""
        };
        return _this;
    }

    _createClass(PersonalContact, [{
        key: "render",
        value: function render() {
            var status = this.state.status;

            return React.createElement(
                "div",
                { "class": "row" },
                React.createElement(
                    "div",
                    { "class": "col-lg-8 col-lg-offset-2" },
                    React.createElement(
                        "form",
                        { name: "sentMessage", id: "contactForm", onSubmit: this.submitForm, action: "https://formspree.io/xpzypzqk", method: "POST" },
                        React.createElement(
                            "div",
                            { "class": "row control-group" },
                            React.createElement(
                                "div",
                                { "class": "form-group col-xs-12 floating-label-form-group controls" },
                                React.createElement(
                                    "label",
                                    null,
                                    "Name"
                                ),
                                React.createElement("input", { type: "text", name: "name", "class": "form-control", placeholder: "Name", id: "name", required: true, "data-validation-required-message": "Please enter your name." }),
                                React.createElement("p", { "class": "help-block text-danger" })
                            )
                        ),
                        React.createElement(
                            "div",
                            { "class": "row control-group" },
                            React.createElement(
                                "div",
                                { "class": "form-group col-xs-12 floating-label-form-group controls" },
                                React.createElement(
                                    "label",
                                    null,
                                    "Email Address"
                                ),
                                React.createElement("input", { type: "email", name: "email", "class": "form-control", placeholder: "Email Address", id: "email", required: true, "data-validation-required-message": "Please enter your email address." }),
                                React.createElement("p", { "class": "help-block text-danger" })
                            )
                        ),
                        React.createElement(
                            "div",
                            { "class": "row control-group" },
                            React.createElement(
                                "div",
                                { "class": "form-group col-xs-12 floating-label-form-group controls" },
                                React.createElement(
                                    "label",
                                    null,
                                    "Phone Number"
                                ),
                                React.createElement("input", { type: "tel", name: "telephone", "class": "form-control", placeholder: "Phone Number", id: "phone", required: true, "data-validation-required-message": "Please enter your phone number." }),
                                React.createElement("p", { "class": "help-block text-danger" })
                            )
                        ),
                        React.createElement(
                            "div",
                            { "class": "row control-group" },
                            React.createElement(
                                "div",
                                { "class": "form-group col-xs-12 floating-label-form-group controls" },
                                React.createElement(
                                    "label",
                                    null,
                                    "Message"
                                ),
                                React.createElement("textarea", { rows: "5", name: "message", "class": "form-control", placeholder: "Message", id: "message", required: true, "data-validation-required-message": "Please enter a message." }),
                                React.createElement("p", { "class": "help-block text-danger" })
                            )
                        ),
                        React.createElement(
                            "button",
                            null,
                            "Submit"
                        ),
                        status === "SUCCESS" && React.createElement(
                            "p",
                            null,
                            "Thanks!"
                        ),
                        status === "ERROR" && React.createElement(
                            "p",
                            null,
                            "There appears to be a problem. Try disabling lastpass on this page. "
                        )
                    )
                )
            );
        }
    }, {
        key: "submitForm",
        value: function submitForm(ev) {
            var _this2 = this;

            ev.preventDefault();
            var form = ev.target;
            var data = new FormData(form);
            var xhr = new XMLHttpRequest();
            xhr.open(form.method, form.action);
            xhr.setRequestHeader("Accept", "application/json");
            xhr.onreadystatechange = function () {
                if (xhr.readyState !== XMLHttpRequest.DONE) return;
                if (xhr.status === 200) {
                    form.reset();
                    _this2.setState({ status: "SUCCESS" });
                } else {
                    _this2.setState({ status: "ERROR" });
                }
            };
            xhr.send(data);
        }
    }]);

    return PersonalContact;
}(React.Component);

el = function el() {
    return React.createElement(
        "p",
        null,
        "hi"
    );
};
var domContainer = document.getElementById('contactDiv');
ReactDOM.render(el, domContainer);