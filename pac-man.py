"""Launch Pac-Man using the command required by the subject."""

if __name__ == "__main__":
    try:
        from src.__main__ import main
    except ImportError as error:
        print(f"Pac-Man: Missing dependency: {error}. Run 'make install'.")
        raise SystemExit(1) from None
    raise SystemExit(main())
