import pylink


"""
Building blocks
"""


def initialize_tracker(ip_address="100.1.1.1"):
    """
    Initialize a connection to the EyeLink tracker.
    :param ip_address: The IP address of the EyeLink tracker.
    :return: A connection to the tracker.
    """
    try:
        # Connect to the EyeLink tracker using the specified IP address
        tracker = pylink.EyeLink(ip_address)
        print("Successfully connected to the EyeLink tracker.")
        return tracker
    except RuntimeError as e:
        print(f"Failed to connect to the EyeLink tracker: {e}")
        return None

if __name__ == "__main__":
    # Replace '100.1.1.1' with your tracker's IP address if different
    tracker = initialize_tracker("100.1.1.1")
    if tracker:
        # Additional setup or operations here
        
        # When done, close the connection
        tracker.close()
