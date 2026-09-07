function CourseList({ courses }) {
    return (
        <div>
            {/* // mb-4 is a Tailwind CSS class that adds a margin-bottom of 1rem (16px) to the element. This is used to create space between the heading and the list of courses.
            // text-xl is a Tailwind CSS class that sets the font size of the element to 1.25rem (20px). This is used to make the heading larger and more prominent.
            // font-semibold is a Tailwind CSS class that sets the font weight of the element to 600. This is used to make the heading bold and stand out. */}
            <h2 className="mb-4 text-xl font-semibold">
                Meine Kurse
            </h2>

            {/* // grid is used to create a grid layout for the courses.
            // gap-4 is used to add a gap of 1rem (16px) between the grid items.
            // md:grid-cols-2 is used to set the number of columns in the grid to 2 on medium screens and above.
            // lg:grid-cols-3 is used to set the number of columns in the grid to 3 on large screens and above. */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {courses.map((course) => (
                // rounded-xl is used to round the corners of the course card. xl is used to set the border radius to 1rem (16px).
                // bg-white is used to set the background color of the course card to white.
                // p-5 is used to add padding of 1.25rem (20px) to the course card. padding is used to create space between the content of the card and its border.
                // shadow-sm is used to add a small shadow to the course card. This is used to create a sense of depth and make the card stand out from the background.
                    <div key={course.id} className="rounded-xl bg-white p-5 shadow-sm">
                        <h3 className="font-semibold"> {course.fullname} </h3>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CourseList;