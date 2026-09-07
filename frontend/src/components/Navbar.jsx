function Navbar({ handleLogout }) {

    // Navbar component that displays the title and a logout button. The handleLogout function is passed as a prop from the parent component (App) and is called when the logout button is clicked.
    // mb-8: margin-bottom: 2rem (32px)
    // flex: display: flex
    // flex is used to create a flexible layout for the navbar. It allows the title and the logout button to be aligned horizontally and spaced apart.
    // items-center: align-items: center
    // justify-between is used to space the title and the logout button apart, with the title on the left and the button on the right.
    return (
        <div className="mb-8 flex items-center justify-between">
            <h1 className="text-3xl font-bold">
                Moodle Organizer
            </h1>


            {/* // rounded-lg is used to round the corners of the logout button. lg is used to set the border radius to 0.5rem (8px).
            // border is used to add a border to the logout button. The default color is gray.
            // border-gray-300 is used to set the color of the border to a light gray. 300 is used to set the shade of gray. The higher the number, the darker the color.
            // bg-white ist used to set the background color of the logout button to white.
            // px-4 is used to add padding of 1rem (16px) to the left and right of the logout button.
            // py-2 is used to add padding of 0.5rem (8px) to the top and bottom of the logout button.
            // hover:bg-gray-50 is used to change the background color of the logout button to a very light gray when the user hovers over it. 50 is used to set the shade of gray. The higher the number, the darker the color. */}
            <button
                onClick={handleLogout}
                className="rounded-lg border border-gray-300 bg-white px-4 py-2 hover:bg-gray-50">
                Logout
            </button>
        </div>
    );

}

export default Navbar;