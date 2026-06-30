# frozen_string_literal: true

require 'date'
require 'time'

module Jekyll
  module DateRoFilter
    MONTHS = {
      1 => 'ianuarie', 2 => 'februarie', 3 => 'martie', 4 => 'aprilie',
      5 => 'mai', 6 => 'iunie', 7 => 'iulie', 8 => 'august',
      9 => 'septembrie', 10 => 'octombrie', 11 => 'noiembrie', 12 => 'decembrie'
    }.freeze

    MONTHS_SHORT = {
      1 => 'ian', 2 => 'feb', 3 => 'mar', 4 => 'apr', 5 => 'mai', 6 => 'iun',
      7 => 'iul', 8 => 'aug', 9 => 'sep', 10 => 'oct', 11 => 'noi', 12 => 'dec'
    }.freeze

    def date_ro(input, format = 'long')
      return input if input.nil? || input.to_s.strip.empty?

      date = parse_date(input)
      return input unless date

      months = format == 'short' ? MONTHS_SHORT : MONTHS
      "#{date.day} #{months[date.month]} #{date.year}"
    end

    def format_mdl(input)
      return input if input.nil? || input.to_s.strip.empty?

      num = input.to_f
      whole = num.round
      whole.to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1 ').reverse
    end

    def currency_code(input)
      return input if input.nil? || input.to_s.strip.empty?

      code = input.to_s.strip.upcase
      case code
      when 'EURO', 'EUR' then 'EUR'
      when 'LEI', 'LEU' then 'RON'
      else code
      end
    end

    private

    def parse_date(input)
      return input if input.is_a?(Date)

      Time.parse(input.to_s).to_date
    rescue StandardError
      nil
    end
  end
end

Liquid::Template.register_filter(Jekyll::DateRoFilter)
