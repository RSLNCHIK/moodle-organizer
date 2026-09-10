function BackgroundTile({ accented = false }) {
    // Nur wenige Felder sind schon ohne Maus leicht eingefaerbt.
    // Tailwind steuert Transparenz und Nachleuchten direkt im className.
    // ease-[ease-out] is used to set the easing function for the transition to ease-out, which makes the transition start quickly and then slow down towards the end.
    // hover:bg-[#8b5cf6]/14 is used to set the background color of the element to a semi-transparent purple color when the user hovers over it.
    // hover:duration-150 is used to set the duration of the transition to 150ms when the user hovers over the element.
    // motion-reduce:transition-none is used to disable transitions for users who have requested reduced motion in their operating system settings.
    // ${accented ? "bg-[#8b5cf6]/9" : "bg-transparent"} is used to conditionally set the background color of the element based on the a prop. If accented is true, the background color is set to a semi-transparent purple color, otherwise it is set to transparent.
    return (
        <div
            aria-hidden="true"
            className={`
                transition-colors duration-[1200ms] ease-[ease-out]
                hover:bg-[#8b5cf6]/14 hover:duration-150
                motion-reduce:transition-none
                ${accented ? "bg-[#8b5cf6]/9" : "bg-transparent"}
            `}
        />
    );
}

export default BackgroundTile;
