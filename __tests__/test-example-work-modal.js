import React from "react";
import { shallow } from "enzyme";
import ExampleWorkModal from "../js/example-work-modal";
import Enzyme from "enzyme";
import Adapter from "enzyme-adapter-react-16";
Enzyme.configure({ adapter: new Adapter() });

const myExample = {
  title: "Work Example",
  href: "https://example.com",
  desc: "Long description",
  image: {
    desc: "example screenshot of a project involving code",
    src: "images/example1.png",
    comment: ""
  }
};

describe("ExampleWorkModal Component", () => {
  let mockCloseModalFn = jest.fn();
  let component = shallow(
    <ExampleWorkModal
      example={myExample}
      open={false}
      closeModal={mockCloseModalFn}
    />
  );
  let openComponent = shallow(
    <ExampleWorkModal example={myExample} open={true} />
  );

  let anchors = component.find("a");

  it("Should properly open and hide", () => {
    expect(
      component.find(".background--skyBlue").hasClass("modal--closed")
    ).toBe(true);
    expect(
      openComponent.find(".background--skyBlue").hasClass("modal--open")
    ).toBe(true);
  });
  it("Should contain a single anchor element", () => {
    expect(anchors.length).toEqual(1);
  });
  it("Should link to our project", () => {
    expect(anchors.prop("href")).toEqual(myExample.href);
  });
  it("Should call closeModal when clicked", () => {
    component.find(".modal__closeButton").simulate("click");
    expect(mockCloseModalFn).toHaveBeenCalled();
  });
});
