import stripe


class PayError(stripe.error.StripeError):
    pass
