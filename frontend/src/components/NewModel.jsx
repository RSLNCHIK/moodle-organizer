import BackgroundTile from "./BackgroundTile";

function NewModel({ onContinue }) {

    // 8 Spalten mal 5 Reihen: ein begrenztes Raster hinter dem Inhalt.
    // Die Nummern bleiben gleich, damit React jedes Kaestchen wiedererkennt.
    // relative is used to set the position of the container to relative, which allows the child elements to be positioned relative to the container.
    // isolate is used to create a new stacking context for the container, which prevents the child elements from being affected by the z-index of other elements on the page.
    // min-h is used to set the minimum height of the container to 100% of the viewport height, which ensures that the container takes up the full height of the screen.
    // overflow-hidden is used to hide any content that overflows the container, which prevents scrollbars from appearing on the page.
    // Tailwind positioniert das Raster mittig. Die Maske blendet seine Raender aus.
    const tiles = Array.from({ length: 40 }, (_, index) => index);
    const accentTiles = [5, 14, 33, 38];

    return (
        <div className="relative isolate min-h-screen overflow-hidden bg-white">
            <div
                aria-hidden="true"
                className="
                    absolute top-0 left-1/2 z-0 -translate-x-1/2 grid
                    [--tile-size:clamp(96px,9.6vw,126px)]
                    grid-cols-[repeat(8,var(--tile-size))]
                    grid-rows-[repeat(5,var(--tile-size))]
                    w-[calc(8*var(--tile-size))] h-[calc(5*var(--tile-size))]
                    bg-[linear-gradient(to_right,rgb(139_92_246_/_0.14)_1px,transparent_1px),linear-gradient(to_bottom,rgb(139_92_246_/_0.14)_1px,transparent_1px)]
                    bg-size-[var(--tile-size)_var(--tile-size)]
                    mask-[radial-gradient(ellipse_at_center,black_20%,transparent_72%)]
                ">
                {tiles.map((tileId) => (
                    <BackgroundTile key={tileId} accented={accentTiles.includes(tileId)} />
                ))}
            </div>
            
            {/* Dieser Container umfasst den gesamten Inhalt und liegt über dem Raster. */}
            <div className="relative z-10 pointer-events-none max-w-340 mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-10">
                {/* <!-- Announcement Banner --> */}
                {/* // bg-layer is used to set the background color of the banner to a layer color defined in the Tailwind CSS configuration. 
                pointer-events-auto is used to enable pointer events on the element.
                inline-flex is used to set the display property of the element to inline-flex, which makes it a flexible inline-level element.
                border-s is used to set the border style of the element to a solid line on the left side. */}
                <div className="flex justify-center">
                    <a className="pointer-events-auto inline-flex items-center gap-x-2 bg-layer border border-layer-line text-xs text-layer-foreground p-2 px-3 rounded-full transition hover:border-line-3 focus:outline-hidden focus:border-line-3" href="#">
                        Explore the Capital Product
                        <span className="flex items-center gap-x-1">
                            <span className="border-s border-line-2 text-primary ps-2">Explore</span>
                            <svg className="shrink-0 size-4 text-primary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6" /></svg>
                        </span>
                    </a>
                </div>
                {/* <!-- End Announcement Banner -->
                max-w-4xl is used to set the maximum width of the container to 64rem (1024px).
                mx-auto is used to center the container horizontally in the viewport. mx stands for margin-left and margin-right
                block is used to set the display property of the element to block, which makes it take up the full width of its parent container.
                m-0 is used to set the margin of the element to 0, which removes any default margin that may be applied.
                text-slate-800 is used to set the text color of the element to a dark gray color defined in the Tailwind CSS configuration.
                md:text-5xl is used to set the font size of the element to 3rem (48px) on medium-sized screens and larger.
                leading-tight is used to set the line height of the element to 1.25, which makes the lines of text closer together.
                <!-- Title --> */}
                <div className="mt-8 max-w-4xl text-center mx-auto">
                    <h1 className="m-0 font-bold text-slate-800 text-4xl md:text-5xl lg:text-7xl leading-tight">
                        Supercharged Preline Experience
                    </h1>
                </div>
                {/* <!-- End Title --> */}

                <div className="mt-5 max-w-3xl text-center mx-auto">
                    <p className="text-lg text-muted-foreground-2">Preline is a large open-source project, crafted with Tailwind CSS framework by Hmlstream.</p>
                </div>

                {/* <!-- Buttons --> */}
                <div className="mt-8 gap-3 flex justify-center">
                    <button
                        type="button"
                        onClick={onContinue}
                        className="pointer-events-auto inline-flex cursor-pointer justify-center items-center gap-x-3 text-center bg-linear-to-tl from-violet-600 to-blue-600 hover:from-blue-600 hover:to-violet-600 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-violet-600 text-white text-sm font-medium rounded-full py-3 px-4"
                    >
                        Continue with Moodle
                        <svg aria-hidden="true" className="shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M5 12h14m-6-6 6 6-6 6" />
                        </svg>
                    </button>
                </div>
                {/* <!-- End Buttons --> */}

            </div>
        </div>
        // <!-- End Hero -->
    )

}

export default NewModel;
