from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payments, User


class PaymentsSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = Payments
        fields = ['id', 'user', 'course', 'lesson', 'payment_amount', 'payment_date', 'payment_method', 'payments']

    def get_payments(self, obj):
        if obj.course:
            related_payments = obj.course.payments.all()  # Получаем все платежи для курса
        elif obj.lesson:
            related_payments = obj.lesson.payments.all()  # Получаем все платежи для урока
        else:
            return []  # Возвращаем пустой список, если нет ни курса, ни урока
        # Сериализация связанных платежей
        return PaymentsSerializer(related_payments, many=True).data

    def validate(self, data):
        """ Проверка, что хотя бы одно из полей course или lesson заполнено. """
        if not data.get('course') and not data.get('lesson'):
            raise serializers.ValidationError("Оплата должна быть привязана либо к курсу, либо к уроку.")
        return data

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "city")